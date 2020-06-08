from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import requests

app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/mars')

@app.route("/scrape_news")
def mars_news():
    mars_url = 'https://mars.nasa.gov/news'
    pull = requests.get(mars_url)
    soup = bs(pull.text, 'lxml')

    articles = soup.find_all('div', class_='image_and_description_container')

    for article in articles:
        short = article.find('div', class_='rollover_description_inner').text

    # Title code isn't working. The scrape doesn't appear to be pulling the section of code with the title list in it
    #     title = article.find('div', class_='bottom_gradient')
    #     print(title)

        return short

@app.route("/scrape_jpl")
def jpl_mars():
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    html = browser.html
    parse = bs(html,'html.parser')
    info = parse.find_all('article', class_='carousel_item')
    fancybox = info[0]('a')

    for a in fancybox:
        my_link = a['data-fancybox-href']

    featured_image_url = 'https://www.jpl.nasa.gov' + my_link
    return featured_image_url


@app.route("/scrape_facts")
def mars_facts():
    mars_facts_url = 'https://space-facts.com/mars/'
    facts_pull = requests.get(mars_facts_url)
    soup_facts = bs(facts_pull.text, 'lxml')

    mars_tables = soup_facts.find_all('table', class_= 'tablepress tablepress-id-p-mars')
    return mars_tables


@app.route("/scrape_hemispheres")
def mars_hemispheres():
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    img_list = []

    img_root = 'https://astrogeology.usgs.gov/'

    cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(cerberus_url)
    html = browser.html
    cerb_parse = bs(html, 'html.parser')
    cerb_info = cerb_parse.find_all('div', class_='wide-image-wrapper')

    for item in cerb_info:
        cerb_end = item.find('img', class_='wide-image')['src']
        cerb_img = img_root + cerb_end

    schiap_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(schiap_url)
    html = browser.html
    schiap_parse = bs(html, 'html.parser')
    schiap_info = schiap_parse.find_all('div', class_='wide-image-wrapper')

    for item in schiap_info:
        schiap_end = item.find('img', class_='wide-image')['src']
        schiap_img = img_root + schiap_end


    syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis_url)
    html = browser.html
    syrtis_parse = bs(html, 'html.parser')
    syrtis_info = syrtis_parse.find_all('div', class_='wide-image-wrapper')

    for item in syrtis_info:
        syrtis_end = item.find('img', class_='wide-image')['src']
        syrtis_img = img_root + syrtis_end


    valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles_url)
    html = browser.html
    valles_parse = bs(html, 'html.parser')
    valles_info = valles_parse.find_all('div', class_='wide-image-wrapper')

    for item in valles_info:
        valles_end = item.find('img', class_='wide-image')['src']
        valles_img = img_root + valles_end


    img_list.append(cerb_img)
    img_list.append(schiap_img)
    img_list.append(syrtis_img)
    img_list.append(valles_img)


    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hem_titles_images = []
    title_list = []

    html = browser.html
    hem_parse = bs(html,'html.parser')
    hem_info = hem_parse.find_all('div', class_='item')

    for item in hem_info:
        titlehead = item.find('h3').text
        title_list.append(titlehead)
        if titlehead == 'Cerberus Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": cerb_img})
        elif titlehead == 'Schiaparelli Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": schiap_img})
        elif titlehead == 'Syrtis Major Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": syrtis_img})
        elif titlehead =='Valles Marineris Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": valles_img})
   
    browser.quit()

    return jsonify(hem_titles_images)


@app.route("/")
def html():

    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    img_list = []

    img_root = 'https://astrogeology.usgs.gov/'

    cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(cerberus_url)
    html = browser.html
    cerb_parse = bs(html, 'html.parser')
    cerb_info = cerb_parse.find_all('div', class_='wide-image-wrapper')

    for item in cerb_info:
        cerb_end = item.find('img', class_='wide-image')['src']
        cerb_img = img_root + cerb_end

    schiap_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(schiap_url)
    html = browser.html
    schiap_parse = bs(html, 'html.parser')
    schiap_info = schiap_parse.find_all('div', class_='wide-image-wrapper')

    for item in schiap_info:
        schiap_end = item.find('img', class_='wide-image')['src']
        schiap_img = img_root + schiap_end


    syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis_url)
    html = browser.html
    syrtis_parse = bs(html, 'html.parser')
    syrtis_info = syrtis_parse.find_all('div', class_='wide-image-wrapper')

    for item in syrtis_info:
        syrtis_end = item.find('img', class_='wide-image')['src']
        syrtis_img = img_root + syrtis_end


    valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles_url)
    html = browser.html
    valles_parse = bs(html, 'html.parser')
    valles_info = valles_parse.find_all('div', class_='wide-image-wrapper')

    for item in valles_info:
        valles_end = item.find('img', class_='wide-image')['src']
        valles_img = img_root + valles_end


    img_list.append(cerb_img)
    img_list.append(schiap_img)
    img_list.append(syrtis_img)
    img_list.append(valles_img)


    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hem_titles_images = []
    title_list = []

    html = browser.html
    hem_parse = bs(html,'html.parser')
    hem_info = hem_parse.find_all('div', class_='item')

    for item in hem_info:
        titlehead = item.find('h3').text
        title_list.append(titlehead)
        if titlehead == 'Cerberus Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": cerb_img})
        elif titlehead == 'Schiaparelli Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": schiap_img})
        elif titlehead == 'Syrtis Major Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": syrtis_img})
        elif titlehead =='Valles Marineris Hemisphere Enhanced':
            hem_titles_images.append({"Title":titlehead, "img_url": valles_img})
   
    browser.quit()

    return render_template('index.html', dictionary=hem_titles_images)
    mongo.db.collection.update({},hem_titles_images)

if __name__ == "__main__":
    app.run(debug=True)