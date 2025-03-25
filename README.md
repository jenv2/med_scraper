# About med_scraper
This web scraper extracts article titles, abstracts, and URLs from PubMed search results between specified dates for a list of anatomical or physiological system searches between.

This program exports the extracted article data into one master CSV and individual CSVs for each different system. The list of system searches are separated by a new line in a text file titled keywords.txt.

In this project, 'systems' initially referred to different radiology categories, such as Neuroradiology, Gastrointestinal, and Fetal. However, the framework could also be applied to broader anatomical or physiological systems in other medical contexts.

# How to Run

## Run the following command in your terminal:
```py "<path for med_scraper.py>" --startmonth <MM> --startday <DD> --startyear <YYYY> --endmonth <MM> -- endday <DD> --endyear <YYYY>```

For example, run ```py "C:\Users\Jennifer Vaughn\med_scraper\med_scraper.py" --startmonth 12 --startday 1 --startyear 2024 --endmonth 1 --endday 1 --endyear 2025``` to find search results from 12/1/24 to 1/1/25.
