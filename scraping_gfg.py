from bs4 import BeautifulSoup as bs
import requests
import csv
import time

start = time.time()
with open('gfg_scrape.csv', 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['page_nos', 'article_title',
                        'article_link', 'article_hint', 'article_tags'])

    # Scraping first 100 pages of GeeksforGeeks
    for i in range(1, 100):

        url = f'https://www.geeksforgeeks.org/page/{i}/'
        source = requests.get(url).text
        soup = bs(source, 'lxml')


        try:
        # All the aricles in a page are wrapped inside the "div<class=articles-list>"
            articles_list = soup.find('div', class_='articles-list')
        except Exception as e:
            print('Error during extracting articles_list', e)

        try:
            # Each article is wrapped inside a "div<class=content>"
            # Returns a list of all articles
            articles = articles_list.find_all('div', class_='content')

            # Looping over each article and extracting the desired stuff
            for article in articles:
                article_title = article.find('div', class_='head').text
                article_link = article.find('div', class_='head').a['href']
                article_hint = article.find(
                    'div', class_='text').text.replace('Read More', '')
                article_tags = article.find('div', class_='tags').div.find_all(
                    'div', class_='tags-list_item')
                article_tags_list = ', '.join([tag.text for tag in article_tags])

                csv_writer.writerow([i, article_title, article_link, article_hint, article_tags_list])
                print('Written page:', i)
        except Exception as e:
            print('Error during extracting all stuff', e)


            # print(article_title)
            # print(article_link)
            # print(article_hint)
            # print(article_tags_list)
            # print('\n\n')
end = time.time()
print(end - start)

import pandas as pd
pd.read_csv('gfg_scrape.csv')
