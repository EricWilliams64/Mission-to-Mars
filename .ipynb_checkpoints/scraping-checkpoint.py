#import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #intialize headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {    
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data


def mars_news(browser):
    #visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        #use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()    
        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    #visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        #find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None    

    #use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #convert DF into html format, add bootstrap
    return df.to_html()



if __name__  == "__main__":
    #if running script, print the data
    print(scrape_all())