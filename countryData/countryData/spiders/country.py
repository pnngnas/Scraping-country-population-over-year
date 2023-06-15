import scrapy


class CountrySpider(scrapy.Spider):
    name = "country"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):
        countries = response.xpath("//table//tr//a")
        for country in countries:
            name = country.xpath("./text()").get()
            link = country.xpath("./@href").get()
            yield response.follow(url = link, meta = {
                'name': name,
            }, callback = self.parse_country)

    def parse_country(self, response):
        rows = response.xpath("(//table)[2]//tbody/tr")
        for row in rows:
            year = row.xpath("(./td)[1]/text()").get()
            population = row.xpath("(./td)[2]/strong/text()").get()
            yield {
                'country': response.request.meta["name"],
                'year' : year,
                'population' : population
            }