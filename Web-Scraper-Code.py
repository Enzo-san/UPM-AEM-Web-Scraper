import requests
import json
from bs4 import BeautifulSoup

def node_spider(max_nodes):
    node = 1
    data = {}
    data['page_data'] = []
    
    while (node <= max_nodes):
        url_string = "https://www1.upm.edu.ph/node/" + str(node)
        source_code = requests.get(url_string)
        plain_text = source_code.text

        soup = BeautifulSoup(plain_text)

        body_text = "" #span tags
        body_paragraph = "" #p tags
        image_links_list = []
        attachment_links_list = []

        #Title Grab
        for link in soup.findAll('h1', {'id': 'page-title'}):
            page_title = link.string #grabs title itself using ".string" method

        
        #Body Grab        
        for link in soup.findAll('span', {'style': 'font-family:arial,helvetica,sans-serif'}):
            body_text += link.text #grabs title itself using ".string" method

        for link in soup.findAll('p'):
            body_paragraph += link.text #grabs title itself using ".string" method

        #Image Grab
        for link in soup.findAll('img', {'class': 'img-responsive'}):
            image_link = link.get('src')
            image_links_list.append(str(image_link))

        #Image Grab
        for link in soup.findAll('a'):
            attachment_link = link.get('href')
            if attachment_link is not None and "pdf" in attachment_link:
                print(node)
                print(": ok")
                attachment_links_list.append(str(attachment_link))
            else:
                pass

        node += 1

        #Writing to JSON
        data['page_data'].append({
            'URL': url_string,
            'NODE_NUMBER': node-1,
            'PAGE_TITLE': page_title,
            'BODY_TEXT_SPAN': str(body_text), #span tags
            'BODY_TEXT_PARAGRAPH': str(body_paragraph), #p tags
            'IMG_SOURCES': image_links_list,
            'ATTACHMENT_LINKS': attachment_links_list
        })

    with open('data.json', 'w') as page_file:
        json.dump(data, page_file)

node_spider(3252) #Change param to maximum available node number from the www1 website
#max = 3252