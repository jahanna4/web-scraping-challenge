from bs4 import BeautifulSoup as bs
from splinter import Browser
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
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
# def mars_facts():
#     mars_facts_url = 'https://space-facts.com/mars/'
#     facts_pull = requests.get(mars_facts_url)
#     soup_facts = bs(facts_pull.text, 'lxml')

#     mars_tables = soup_facts.find_all('table', class_= 'tablepress tablepress-id-p-mars')
#     return jsonify(mars_tables)

# def jpl_mars():
    # executable_path = {'executable_path':'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)
    # jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(jpl_url)


    # html = browser.html
    # parse = bs(html,'html.parser')
    # info = parse.find_all('article', class_='carousel_item')
    # fancybox = info[0]('a')

    # for a in fancybox:
    #     my_link = a['data-fancybox-href']

    # featured_image_url = 'https://www.jpl.nasa.gov' + my_link
    # return featured_image_url

if __name__ == "__main__":
    app.run(debug=True)