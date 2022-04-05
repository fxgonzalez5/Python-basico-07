import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        link = response.url.split("/page")[-2]
        filename = f'datos/quotes-url1-{page}.csv'
        with open(filename, 'a') as f:
            datos = response.xpath("""//div[@class='col-md-4 tags-box']/span/a/@href""").extract()
            # datos = response.xpath("""//div[@class='col-md-4 tags-box']/span/a""").extract()
            for d in datos:
                urlTag = link+d
                print(urlTag)
                f.write("%s\n" % urlTag)