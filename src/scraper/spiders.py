import scrapy

class GeneralDataSpider(scrapy.Spider):
    name = 'soccerscraper'
        
    def parse(self, response):
        raw_data = response.css('.standard_tabelle ::text').extract()
        data = [element.strip() for element in raw_data]
        data = [element for element in data if element != '']
        
        season_and_league_match = response.css('.breadcrumb ::text').extract()[1]
        self.outputResponse['general'].append((season_and_league_match, data))
        
class HomeDataSpider(scrapy.Spider):
    name = 'soccerscraper'
        
    def parse(self, response):
        raw_data = response.css('.standard_tabelle ::text').extract()
        data = [element.strip() for element in raw_data]
        data = [element for element in data if element != '']
        
        season_and_league_match = response.css('.breadcrumb ::text').extract()[1]
        self.outputResponse['home'].append((season_and_league_match, data))
        
class AwayDataSpider(scrapy.Spider):
    name = 'soccerscraper'
        
    def parse(self, response):
        raw_data = response.css('.standard_tabelle ::text').extract()
        data = [element.strip() for element in raw_data]
        data = [element for element in data if element != '']
        
        season_and_league_match = response.css('.breadcrumb ::text').extract()[1]
        self.outputResponse['away'].append((season_and_league_match, data))