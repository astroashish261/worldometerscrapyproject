import scrapy


class CoronavirusSpider(scrapy.Spider):
    name = 'coronavirus'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/coronavirus']

    def parse(self, response):
        for country in response.xpath("(//tr/td/a)[@class ='mt_a']"):
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            #absolute_url = f"https://www.worldometers.info/coronavirus/{link}"
            #absolute_url = response.urljoin(link)
            if link:
              yield response.follow(url=link, callback= self.page2parser, meta = {'country_name':name})

    def page2parser(self, response):
        country_names = response.request.meta["country_name"]
        cases = response.xpath("((//div)[@class = 'maincounter-number'])[1]/span/text()").get()
        deaths = response.xpath("((//div)[@class = 'maincounter-number'])[2]/span/text()").get()
        recovered = response.xpath("((//div)[@class = 'maincounter-number'])[3]/span/text()").get()
        yield{
            "country_names":country_names,
            "corona_cases": cases,
            "corona_deaths":deaths,
            "recovered":recovered

        }


                
            
