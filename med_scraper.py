import requests
from bs4 import BeautifulSoup
import time
import csv
import argparse
import pandas as pd

root_pubmed_url = "https://pubmed.ncbi.nlm.nih.gov"
pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/?term="
articles_data = [] #data for all scraped articles

# Extract PMIDs of all articles from a PubMed search result
# Builds a URL to each article
def get_pmids(page, keyword, search_number, startmonth, startday, startyear, endmonth, endday, endyear):
    search = keyword['search']
    
    # URL to one unique page of results for a keyword search
    url = f'{pubmed_url}+{search}+ AND ({startyear}/{startmonth}/{startday}:{endyear}/{endmonth}/{endday}[pdat])+&page={page}'

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch search results for search {search_number}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    #find section which holds the PMIDs for all articles on the page
    pmids = []
    pmids = soup.find('meta',{'name':'log_displayeduids'})['content']

    for pmid in pmids.split(','):
        article_url = root_pubmed_url + '/' + pmid
        article_data = extract_by_article(article_url, keyword)
        if article_data:
            articles_data.append(article_data)
        time.sleep(0.5) #avoid overwhelming the server
    print(f"{len(pmids.split(','))} article(s) have just been extracted for search {search_number}.")
    
def extract_by_article(url, keywords):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch article: {url}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
 
    #Get article title
    try:
        title = soup.find('meta',{'name':'citation_title'})['content'].strip('[]')
    except:
        title = 'NO_TITLE'

    #Get article abstract
    try:
        abstract = soup.find('div', class_='abstract-content selected').get_text(strip=True)
    except:
        abstract = 'NO_ABSTRACT'

    #Get journal title
    try:
        journal = soup.find('meta',{'name':'citation_journal_title'})['content']
    except:
        journal = 'NO_JOURNAL'

    article_data = {
        'Title': title,
        'Abstract': abstract,
        'Journal': journal,
        'URL': url,
        'SYSTEM': keywords['system']
    }

    #add this article dict to list of all article dicts
    articles_data.append(article_data)

#Gets number of pages returned by search results
def get_num_pages(keyword, startmonth, startday, startyear, endmonth, endday, endyear):
    search = keyword['search']
    
    # URL to the first page of results for a keyword search
    search_url = f'{pubmed_url}+{search}+ AND ({startyear}/{startmonth}/{startday}:{endyear}/{endmonth}/{endday}[pdat])'
    
    with requests.get(search_url) as response:
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        pages_span = soup.find('span', {'class': 'total-pages'})
        if pages_span: #if there are multiple pages
            num_pages = int(pages_span.get_text().replace(',',''))
        else: #if there's only 1 page
            num_pages = 1
        
        return num_pages

# Write the search results to CSVs
def write_to_csv(articles_data):
    filename = 'medscraper_all_results.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['SYSTEM', 'Title', 'Abstract', 'Journal', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for article in articles_data:
            writer.writerow(article)

    df = pd.read_csv(filename)
    
    #Now, create separate CSVs for each 'system'
    for system, group in df.groupby('SYSTEM'):
        system_filename = f"medscraper_{system.replace(' ', '_')}.csv"
        group.to_csv(system_filename, index=False, encoding='utf-8')
        #remove duplicates in each system file:
        system_df = pd.read_csv(system_filename)
        system_df = df.drop_duplicates(subset=['URL'], keep='first')
        system_df.to_csv(system_filename, index=False, encoding='utf-8')
        print(f"Created {system_filename}.\n")


if __name__ == "__main__":
    #set options so user can choose publication date range to scrape
    parser = argparse.ArgumentParser(description='Asynchronous PubMed Scraper')
    parser.add_argument('--startmonth', type=int, default=7, help='Specify start month for publication date range to scrape. Default = 7')
    parser.add_argument('--startday', type=int, default=14, help='Specify start day for publication date range to scrape. Default = 14')
    parser.add_argument('--startyear', type=int, default=2024, help='Specify start year for publication date range to scrape. Default = 2024')
    parser.add_argument('--endmonth', type=int, default=8, help='Specify end month for publication date range to scrape. Default = 8')
    parser.add_argument('--endday', type=int, default=14, help='Specify end day for publication date range to scrape. Default = 14')
    parser.add_argument('--endyear', type=int, default=2024, help='Specify end year for publication date range to scrape. Default = 2024')
    args = parser.parse_args()

    #construct our list of keywords from the keywords.txt file
    keywords = []
    with open(r'C:\Users\Jennifer Vaughn\med_scraper\keywords.txt') as file:
        for line in file:
            system, search = line.strip().split('|')
            keywords.append({'system': system, 'search': search})
    print(f'\nFinding PubMed article URLs for {len(keywords)} searches found in keywords.txt\n')
    print(f'Scraping initiated for articles from {args.startmonth}-{args.startday}-{args.startyear} to {args.endmonth}-{args.endday}-{args.endyear}\n')

    # Get and run loop to build a list of all URLs
    completed_searches = 0
    total_searches = len(keywords)
    for keyword in keywords:
        print(f"Starting search {completed_searches+1}/{total_searches}: {keyword['system']}")

        num_pages = get_num_pages(keyword, args.startmonth, args.startday, args.startyear, args.endmonth, args.endday, args.endyear)
        print(f"Number of pages for search {completed_searches+1}/{total_searches}: {num_pages} page(s).")
        if num_pages > 3:
            num_pages = 3
            print(f"Only the first three pages will be extracted.")

        for page in range(1, num_pages+1):
            get_pmids(page, keyword, completed_searches+1, args.startmonth, args.startday, args.startyear, args.endmonth, args.endday, args.endyear)
        
        completed_searches += 1
        print(f"Completed {completed_searches}/{total_searches} searches\n")
    
    write_to_csv(articles_data)
    print("All search results saved to medscraper_all_results.csv.")
