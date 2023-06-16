import scrapy


class GlassesSpider(scrapy.Spider):
    name = "glasses"
    allowed_domains = ["www.glassesshop.com"]
    start_urls = ["https://www.glassesshop.com/bestsellers"]


    def parse(self, res):
        rows = res.xpath('//div[@id="product-lists"]/div')
        for row in rows:
            brand = row.xpath('./div[@class="product-img-outer"]/a[1]/@title').get()
            link = row.xpath('./div[@class="product-img-outer"]/a[1]/@href').get()
            price = row.xpath('./div[@class="p-title-block"]//div[@class="p-price"]//span/text()').get()
            if brand:
                yield {
                    'brand': brand,
                    'img': link,
                    'price': price,
                }
        
        nextpage_url = res.xpath('//li[@class="page-item active"]/following-sibling::li/a/@href').get()
        if nextpage_url:
            yield scrapy.Request(url = nextpage_url, callback=self.parse)

