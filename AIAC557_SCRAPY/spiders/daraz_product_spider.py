from datetime import datetime
from pathlib import Path

import scrapy
import chompjs


class DarazProductSpider(scrapy.Spider):
    name = "daraz_products"
    current_page = 1
    baseurl = "https://www.daraz.com.np/mens-sneakers/"

    def start_requests(self):
        yield scrapy.Request(url=self.baseurl,
                             callback=self.parse,
                             meta={'playwright': True})

    def parse(self, response):
        is_next_page = response.css('.ant-pagination-next::attr(aria-disabled)').get()

        if is_next_page == 'false':
            self.current_page += 1
            yield response.follow("%s?page=%s" % (self.baseurl, str(self.current_page)),
                                  self.parse,
                                  meta={'playwright': True})

        item_links = response.css('.gridItem--Yd0sa div div div div a::attr(href)').getall()
        yield from response.follow_all(item_links,
                                       self.parseProduct,
                                       meta={'playwright': True})

    def parseProduct(self, response):
        sku = ''

        specifications = response.css('.pdp-general-features ul li')
        for s in specifications:
            spec_title = s.css('.key-title::text').get()
            print("SPEC-TITLE:|%s|" % (spec_title))
            if spec_title == ' SKU  ':
                print("SPEC-VALUE: %s" % (s.css('div::text').get()))
                sku = s.css('div::text').get()

        yield {
            'datetime': datetime.now().isoformat(),
            'sku': sku,
            'name': response.css('.pdp-mod-product-badge-title::text').get(),
            'brand': response.css('.pdp-product-brand__brand-link::text').get(),
            'price': response.css('.pdp-price_size_xl::text').get().replace('Rs. ', '').replace(',', ''),
            'categories': response.css('.breadcrumb_item_anchor span::text').getall()
        }
