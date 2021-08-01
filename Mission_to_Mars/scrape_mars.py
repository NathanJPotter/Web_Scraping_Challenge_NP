#!/usr/bin/env python
# coding: utf-8

# In[437]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[438]:


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # Scrape NASA Mars News

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

# # Scape Featured Mars Space Image

def featured_image(browser):


# Visit https://spaceimages-mars.com/
image_url = "https://spaceimages-mars.com/"
browser.visit(image_url)

browser.is_elemnent_present_by_css('div.floating_text_area', wait_time=1)

# Scape image_page into Soup
image_html = browser.html
image_soup = bs(image_html, "html.parser")


# In[446]:


# Find FULL IMAGE button
button_elem = image_soup.select_one('div.floating_text_area')
button_elem


# In[447]:


# Get FULL IMAGE link
full_image_button = button_elem.select_one('a').get("href")
full_image_button


# In[448]:


# Add FULL IMAGE link to base url to get featured image
featured_image_url = image_url + full_image_button
featured_image_url


# # Scrape Mars Facts

# In[449]:


# Get Mars comparison table with pandas 'pd.read_html'

mars_comp_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
mars_comp_df.head()


# In[450]:


# Rename table columns
mars_comp_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
mars_comp_df.set_index('Mars - Earth Comparison', inplace=True)
mars_comp_df


# In[451]:


mars_facts_df = mars_comp_df[1:].reset_index()
mars_facts_df


# # Scrape Images and Titles of Mars Hemispheres

# In[452]:


hem_url = "https://marshemispheres.com/"
browser.visit(hem_url)

time.sleep(1)


# In[453]:


hem_html = browser.html
hem_soup = bs(hem_html, "html.parser")


# In[454]:


# hem_elem = hem_soup.select_one("div.item")
# hem_elem


# In[455]:


# hem_links = hem_elem.select_one('a').get("href")
# hem_links


# In[456]:


# links_url = hem_url + hem_links
# links_url


# In[457]:


# links = browser.find_by_css('h3').click()
# links


# In[464]:


hemisphere_image_urls = []

links = browser.find_by_tag('h3')

for item in links:
    hemisphere = {}
    
    # Loop through each element and click on hemisphere links
    browser.find_by_tag('h3').click()    
        
    # Get hemisphere title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Get url for full resolution image of hemisphere
    sample_link = browser.find_by_text("Sample").first
    hemisphere["img_url"] = sample_link["href"]

    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Return to previous webpage
    browser.back()


# In[465]:


hemisphere_image_urls


# In[ ]:





# In[ ]:


browser.quit()

