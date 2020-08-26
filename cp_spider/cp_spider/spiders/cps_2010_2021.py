import scrapy
import json
import pandas as pd
from scrapy_splash import SplashRequest
from datetime import datetime


class Cps20102021Spider(scrapy.Spider):
    name = 'cps_2010-2021'
    start_urls = [
        'https://www.mas.gov.sg/regulation/regulations-and-guidance?sectors=Capital%20Markets&origin=capital-markets&content_type=Consultations&date=2009-12-30T16%3A00%3A00.000Z%2C2021-01-01T23%3A59%3A59.000Z&page=1&rows=All']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={"wait": 1})

    def parse(self, response):
        titles = response.css(
            '#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li > article > div.ola-field.ola-field-title > div > a > span::text').getall()

        with open('titles.json', 'w') as titles_json:
            titles_list = []
            for title in titles:
                titles_list.append(title)
            titles_json.write(json.dumps(titles_list))

        tags = response.css(
            '#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li > article > footer > div > a > span.ola-flex-content.mas-link__text::text').getall()

        with open('tags.json', 'w') as tags_json:
            tag_list = []
            for tag in tags:
                if tag not in tag_list:
                    tag_list.append(tag)
            tags_json.write(json.dumps(tag_list))

        card_count = len(response.css(
            '#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li > article').getall())

        with open('cards.json', 'w') as cards_json:
            cards = []
            for card_idx in range(1, card_count + 1):

                index = card_idx
                title = response.css(f'#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li:nth-child({card_idx}) > article > div.ola-field.ola-field-title > div > a > span::text').get()
                summary = response.css(f'#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li:nth-child({card_idx}) > article > div.mas-search-card__body > p::text').get()
                tags = response.css(f'#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li:nth-child({card_idx}) > article > footer > div > a > span.ola-flex-content.mas-link__text::text').getall()
                date = response.css(f'#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li > article > header > div > div > div.ts\:xs::text').get()
                link = 'https://www.mas.gov.sg' + response.css(f'#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li:nth-child({card_idx}) > article > div.ola-field.ola-field-title > div > a::attr(href)').get()

                single_card = {'id': index, 'date': date, 'title': title,
                               'summary': summary, 'tags': tags, 'link': link}

                cards.append(single_card)
            # card_list = []
            # for idx, card in enumerate(cards):
            #     card_item = {'id': f'{idx + 1}', 'body': card.css('#mas-search-page > div.mas-search-page__content.g\:12.desktop\(nm-x\:s\) > div > ul > li > article > div.ola-field.ola-field-title > div > a > span')}
            #     card_list.append(card_item)
            # cards_json.write(json.dumps(card_list))
            cards_json.write(json.dumps(cards))

        df = pd.read_json('cards.json')
        df.to_csv('cards.csv', index=None)
