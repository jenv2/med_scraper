# About med_scraper
This web scraper extracts article titles, abstracts, and URLs from PubMed search results between specified dates for a list of anatomical or physiological system searches between.

The list of system searches are separated by a new line in a text file titled keywords.txt. Before running this program, your file path for keywords.txt should be edited within med_scraper.py.

In this project, 'systems' initially referred to different radiology categories, such as Neuroradiology, Gastrointestinal, and Fetal. However, the framework could also be applied to broader anatomical or physiological systems in other medical contexts.

# How to Run

## Run the following command in your terminal:
```py "<path for med_scraper.py>" --startmonth <MM> --startday <DD> --startyear <YYYY> --endmonth <MM> -- endday <DD> --endyear <YYYY>```

For example, run ```py "C:\Users\Jennifer Vaughn\med_scraper\med_scraper.py" --startmonth 12 --startday 1 --startyear 2024 --endmonth 1 --endday 1 --endyear 2025``` to find search results from 12/1/24 to 1/1/25.

## Example output
This program exports the extract article data into one master CSV and individual CSVs for each system. They will be saved within the same directory as med_scraper.py on your machine. The first row of each CSV will be ```SYSTEM  Title  Abstract  Journal  URL```.
