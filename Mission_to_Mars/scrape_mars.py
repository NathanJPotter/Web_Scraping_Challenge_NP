#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# 1. Scrape NASA Mars News

def mars_news(browser):
    # Visit https://redplanetscience.com/
    article_url = "https://redplanetscience.com/"
    browser.visit(article_url)

    browser.is_elemnent_present_by_css('div.list_text', wait_time=1)

    # Scape page into Soup
    art_html = browser.html
    art_soup = bs(art_html, "html.parser")

    try:
        slide_elem = art_soup.select_one('div.list_text')
        latest_news_title = slide_elem.find('div', class_='content_title').get_text()
        news_para = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    return latest_news_title, news_para

# 2. Scape Featured Mars Space Image

def featured_image(browser):
    # Visit https://spaceimages-mars.com/
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    browser.is_elemnent_present_by_css('div.floating_text_area', wait_time=1)

    # Scape image_page into Soup
    image_html = browser.html
    image_soup = bs(image_html, "html.parser")

    try:
        button_elem = image_soup.select_one('div.floating_text_area')
        full_image_button = button_elem.select_one('a').get("href")
        featured_image_url = image_url + full_image_button

    except AttributeError:
        return None, None
    return featured_image_url


# 3. Scrape Mars Facts

def mars_facts():
    try:
        mars_comp_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
        mars_comp_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
        mars_comp_df.set_index('Mars - Earth Comparison', inplace=True)
        mars_facts_df = mars_comp_df[1:].reset_index()
        
        mars_facts_html = mars_facts_df.to_html(justify="left", border="1", classes="table table-sm table-striped table-dark font-weight-light text-align-left", col_space='150px')
    
    except AttributeErroe:
        return None
    
    return mars_facts_html
       

# 4. Scrape Images and Titles of Mars Hemispheres

def hemisphere(browser):
    hem_url = "https://marshemispheres.com/"
    browser.visit(hem_url)

    hem_html = browser.html
    hem_soup = bs(hem_html, "html.parser")
    
    try:
        hemisphere_image_urls = []
        image_links = hem_soup.find_all('div', class_="item")

        for image in range(len(image_links)):
            hemisphere = {}
            
            # Loop through each element and click on hemisphere links
            hem_links = browser.find_by_tag('h3')
            hemlinks[image].click()
            
            hem_html = browser.html
            hem_soup = bs(image_html, 'html.parser')
            
            # Get hemisphere title
            hemisphere["title"] = browser.find_by_css("h2.title").text

            # Get url for full resolution image of hemisphere
            sample_link = browser.find_by_text("Sample").first
            hemisphere["img_url"] = sample_link["href"]


            # Append hemisphere object to list
            hemisphere_image_urls.append(hemisphere)

            # Return to previous webpage
            browser.back()
      
    except AttributeError:
        return None
    
    return hemisphere_image_urls

# This function brings results from the others together
    
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    latest_news_title, news_para = mars_news(browser)
    # featured_image_url = featured_image(browser)
    # mars_facts_df = mars_facts()
    # hemisphere_image_urls = hemisphere(browser)
    # timestamp = dt.datetime.now()

    data = {
        "latest_news_title": latest_news_title,
        "news_para": news_para,
        "featured_image_url": featured_image(browser),
        "mars_facts": mars_facts_df(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data
