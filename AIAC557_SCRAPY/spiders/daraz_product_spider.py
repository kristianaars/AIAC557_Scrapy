from pathlib import Path

import scrapy
import chompjs

class DarazProductSpider(scrapy.Spider):
    name = "daraz_products"

    def start_requests(self):
        urls = [
            "https://www.daraz.com.np/mens-t-shirts/",
        ]
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'playwright': True})


    def parse(self, response):
        item_links = response.css('.gridItem--Yd0sa div div div div a::attr(href)').getall()
        yield from response.follow_all(item_links,
                                       self.parseProduct,
                                       meta={'playwright': True})

    def parseProduct(self, response):
        yield {
            'name': response.css('.pdp-mod-product-badge-title::text').get(),
            'brand': response.css('.pdp-product-brand__brand-link::text').get(),
            'price': response.css('.pdp-price_size_xl::text').get().replace('Rs. ', '').replace(',', ''),
            'categories': response.css('.breadcrumb_item_anchor span::text').getall()
        }