import scrapy
import json

class BBCSpider(scrapy.Spider):
    name = 'bbc'
    start_urls = ['https://www.bbc.com/']

    def parse(self, response):
        li_tags = response.css('li.media-list__item')

        scraped_data = []

        for li_tag in li_tags:
            image_src = li_tag.css('div.responsive-image img::attr(src)').get()

            h3_tag = li_tag.css('h3.media__title')
            title = "No content"
            a_tag = h3_tag.css('a.media__link')
            if a_tag:
                title = a_tag.css('::text').get().strip()


            p_tag = li_tag.css('p.media__summary')
            if p_tag:
                summary = p_tag.css('::text').get().strip()
            else:
                summary = "No content"

            media_tag = li_tag.css('a.media__tag')
            if media_tag:
                tag_content = media_tag.css('::text').get().strip()
            else:
                tag_content = "No content"

            scraped_item = {
                'Image URL': image_src,
                'Title': title,
                'Summary': summary,
                'Tag Content': tag_content
            }

            scraped_data.append(scraped_item)
            self.logger.info("Image URL: %s", image_src)
            self.logger.info("Title: %s", title)
            self.logger.info("Summary: %s", summary)
            self.logger.info("Tag Content: %s", tag_content)
            self.logger.info("-----------------------------")

        with open('output.json', 'w') as file:
            json.dump(scraped_data, file, indent=4)

        self.logger.info("Scraping completed. Data saved as 'output.json'")
