import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BA%D1%83%D0%BB%D0%B8%D0%BD%D0%B0%D1%80%D0%B8%D1%8F/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        next_page = response.xpath("//a[@title= 'Следующая']/@href").get()
        print()

        if next_page:
            yield response.follow(next_page, callback= self.parse)
        for link in links:
            yield response.follow(link, callback= self.parse_books)



    def parse_books (self, response: HtmlResponse):
        url = response.url
        name = response.xpath("//div[@id= 'product-title']/h1/text()").get()
        try:
            author = response.xpath("//a[@data-event-label='author']/@data-event-content").getall()
        except:
            author = 'Не указан'
        basic_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id = 'rate']/text()").get()
        print()
        yield BookparserItem (url = url, name = name, author = author, basic_price = basic_price, discount_price = discount_price, rating = rating)



