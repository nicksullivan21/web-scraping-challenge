# Dependencies
import pandas as pd 
from splinter import Browser
from bs4 import BeautifulSoup as bs 

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    
    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news = soup.find('li', class_='slide')
    newsTitle = news.find('div', class_='content_title').text
    newsText = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images - Featured Image
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    relative_image_path = soup.find_all('img')[1]['src']
    featured_image_url = base_url + relative_image_path

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_table = table[0]
    mars_table = mars_table.rename(columns={0:'Description',1:'Value'},errors='raise')
    mars_table.set_index('Description',inplace=True)
    mars_table = mars_table.to_html()
    mars_table.replace('\n','')

    # Mars Hemispheres
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

# Store data in dictionary
    mars_data = {
        'newsTitle': newsTitle,
        'newsText': newsText,
        'featured_image_url': featured_image_url,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return mars_data
