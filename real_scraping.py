from bs4 import BeautifulSoup
import requests
import json

def trim_spaces(text):
    # Trim leading and trailing spaces
    trimmed_text = text.strip()
    # Replace consecutive spaces with a single space
    trimmed_text = ' '.join(trimmed_text.split())
    return trimmed_text

def scrape_bbc_website():
    url = 'https://www.bbc.com/'  # URL of the BBC website
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    li_tags = soup.find_all('li', class_='media-list__item')
    scraped_data = []
    i = 1
    for li_tag in li_tags:
        url =
        div_tag = li_tag.find('div', class_='responsive-image')
        img_tag = div_tag.find('img')
        image_src = img_tag.get('src')
        news_link = li_tag.find('a', href=True)
        absolute_url = news_link if news_link.startswith('http') else url + news_link

        h3_tag = li_tag.find('h3', class_='media__title')
        if(h3_tag == None):
            title = "No Content" 
        else:
            a_tag = h3_tag.find('a', class_='media__link')
            title = trim_spaces(a_tag.text)
            
        # title = trim_spaces(a_tag.text) if a_tag else "No content"

        p_tag = li_tag.find('p', class_='media__summary')
        if (p_tag == None):
            summary = "No content"
        else:
            summary = trim_spaces(p_tag.text) 

        media_tag = li_tag.find('a', class_='media__tag')
        if (media_tag == None):
            tag_content = "No content"
        else:
            tag_content = trim_spaces(media_tag.text)
        
        if (news_link == None):
            news_link = "No content"
        else:
            news_link = trim_spaces(news_link['href'])

        scraped_item = {
            'Image URL': image_src,
            'Title': title,
            'Summary': summary,
            'Tag Content': tag_content,
            'News Link:': news_link
        }

        scraped_data.append(scraped_item)
        print("No:", i )
        print("Image URL:", image_src)
        print("Title:", title)
        print("Summary:", summary)
        print("Tag Content:", tag_content)
        print("News Link:", news_link)
        print("-----------------------------")
        i = i + 1

    with open('output.json', 'w') as file:
        json.dump(scraped_data, file, indent=4)

    print("Scraping completed. Data saved as 'output.json'")

# Run the scraping function
scrape_bbc_website()
