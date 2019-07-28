from arxivscraper import arxivscraper as scrap
import pandas as pd
import numpy as np
import pickle

#scraping coauthorship information of articles in Math (Quantum Algebra subcategory) from January 1, 2018 to January 20, 2018 
coauthorship_scraper = scrap.Scraper(category='math', date_from='2018-01-01', date_until='2018-01-20', t=10, filters={'categories':['math.qa'],'abstract':['quantum']})
scraped_records = coauthorship_scraper.scrape()

#saving scraped information into pandas dataframe
scraped_columns = ('id', 'title', 'authors')
data_frame = pd.DataFrame(scraped_records, columns = scraped_columns)

#saving pandas dataframe into a .pkl file
data_frame.to_pickle('data.pkl')
