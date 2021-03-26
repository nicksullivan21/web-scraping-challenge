# Dependencies
import pandas as pd 
import datetime as dt 
from splinter import Browser
from bs4 import BeautifulSoup as bs 

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Scrape
def scrape():
    browser = init_browser()

    newsTitle, newsText = mars_news(browser)
    
    mars_info = {
        "newsTitle": newsTitle,
        "newsText": newsText,
        "featured_image_url": featured_image_url(browser),
        "facts": mars_facts(browser),
        "four_hemispheres": mars_hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return mars_info
    
# NASA Mars News
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news = soup.find('li', class_='slide')
    newsTitle = news.find('div', class_='content_title').text
    newsText = soup.find('div', class_='article_teaser_body').text

    return newsTitle, newsText

# JPL Mars Space Images - Featured Image
def featured_image_url(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    relative_image_path = soup.find_all('img')[1]['src']
    featured_image_url = base_url + relative_image_path

    return featured_image_url

    # Mars Facts
def mars_facts(browser):
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_table = table[0]
    mars_table = mars_table.rename(columns={0:'Description',1:'Value'},errors='raise')
    mars_table.set_index('Description',inplace=True)
    mars_table = mars_table.to_html()
    mars_table.replace('\n','')

    return mars_table

# Mars Hemispheres
def mars_hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []
    hemispheres = soup.find_all('div', class_='item')
    for hemisphere in hemispheres:
        hemisphere_dict = {}
        title = hemisphere.find('h3').text
        relative_hemi_path = hemisphere.find('div', class_='description').a['href']
        hemi_url = base_url + relative_hemi_path

        browser.visit(hemi_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        hemisphere_url = soup.find('img', class_='wide-image')['src']

        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = base_url + hemisphere_url
        print(hemisphere_dict['img_url']) 

        hemisphere_image_urls.append(hemisphere_dict)

    return hemisphere_image_urls