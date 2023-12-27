import scrapy
from scrapy.http import Request
from bookScraper.items import BookItem
# from random import randint


class BookspiderSpider(scrapy.Spider):
    name = "bookSpider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # user_agents_list = [
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    #     "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    #     "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    #     "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    #     "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
    #     "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
    # ]

    # custom_settings = {
    #     "FEEDS": {
    #         "bookdata.json": {
    #             "format": "json",
    #             "overwrite": True
    #         }
    #     }
    # } we can define settings here too (instead of settings file)
    
    # def start_requests(self):
    #     return super().start_requests()
    #  or yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            book_page = book.css("h3 a").attrib["href"]

            if "catalogue/" in book_page:
                book_url = "https://books.toscrape.com/" + book_page
            else:
                book_url = "https://books.toscrape.com/catalogue/" + book_page

            # yield response.follow(
            #     book_url,
            #     callback=self.book_parse,
            #     headers={
            #         "User-Agent": self.user_agents_list[
            #             randint(0, len(self.user_agents_list) - 1)
            #         ]
            #     },
            # )
            
            yield response.follow(
                book_url,
                callback=self.book_parse,
            )

        next_page = response.css("li.next a").attrib["href"]

        if next_page:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page

            # yield response.follow(
            #     next_page_url,
            #     callback=self.parse,
            #     headers={
            #         "User-Agent": self.user_agents_list[
            #             randint(0, len(self.user_agents_list) - 1)
            #         ]
            #     },
            # )
            
            yield response.follow(
                next_page_url,
                callback=self.parse,
            )

    def book_parse(self, response):
        table_rows = response.css("table.table.table-striped tr")

        bookItem = BookItem()

        bookItem["url"] = response.url
        bookItem["title"] = response.xpath(
            '//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()'
        ).get()
        bookItem["upc"] = table_rows[0].css("td::text").get()
        bookItem["product_type"] = table_rows[1].css("td::text").get()
        bookItem["price_excl_tax"] = table_rows[2].css("td::text").get()
        bookItem["price_incl_tax"] = table_rows[3].css("td::text").get()
        bookItem["tax"] = table_rows[4].css("td::text").get()
        bookItem["availability"] = table_rows[5].css("td::text").get()
        bookItem["num_reviews"] = table_rows[6].css("td::text").get()
        bookItem["stars"] = response.css("p.star-rating").attrib["class"]
        bookItem["category"] = response.xpath(
            '//*[@id="default"]/div/div/ul/li[3]/a/text()'
        ).get()
        bookItem["description"] = response.xpath(
            '//*[@id="content_inner"]/article/p/text()'
        ).get()
        bookItem["price"] = response.xpath(
            '//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()'
        ).get()

        yield bookItem
