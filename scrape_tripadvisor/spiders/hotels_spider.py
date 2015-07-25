from scrape_tripadvisor.items import HotelItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import re


class TripAdvisorSpider(CrawlSpider):
    name = 'hotels'
    allowed_domains = ['www.tripadvisor.com']
    start_urls = [
        'http://www.tripadvisor.com/'
        'AllLocations-g191-c1-Hotels-United_States.html']
    rules = [
        Rule(LinkExtractor(
            allow='/AllLocations.*'),
            follow=True),
        Rule(
            LinkExtractor(allow='/Hotel_Review.*'),
            callback='parse_hotel_page',
            follow = True
        )
    ]

    def parse_start_url(self, response):
        list(self.parse_hotel_page(response))

    def extract_data(self, response, path):
        values = response.xpath(path).extract()
        if len(values) == 0:
            return ''
        elif len(values) == 1:
            return values[0].strip()
        else:
            values = map(lambda s: s.strip(), values)
            values = filter(None, values)
            return values

    def parse_rating(self, response, nodes_path, rate_path, reviewers_path):
        rating_and_reviewers = []
        nodes = response.xpath(nodes_path)
        for node in nodes:
            rate = self.extract_data(node, rate_path)
            reviewers = self.extract_data(node, reviewers_path)
            rating_and_reviewers.append((rate, reviewers))
        return rating_and_reviewers

    def parse_traveler_rating(self, response):
        return self.parse_rating(response,
            nodes_path="//div[@id='REVIEWS']//ul[@class='barChart']"
                "/div[contains(@class, 'row')]",
            rate_path=".//label[contains(@class,'row')]"
                "//span[@class='text']/text()",
            reviewers_path=".//span[contains(@class,'compositeCount')]"
                "/text()")

    def parse_rating_summary(self, response):
        return self.parse_rating(response,
            nodes_path="//div[@id='SUMMARYBOX']//ul/li",
            rate_path=".//div[@class='name']/text()",
            reviewers_path=".//img/@alt")

    def parse_coordinates(self, response):
        nodes = response.xpath("//script[@type='text/javascript']")
        for node in nodes:
            text = node.extract()
            index = text.find("maps.google.com/maps/api/staticmap?")
            if index != -1:
                link = text[index:index + 300]
                start = 'center='
                end = '&zoom'
                coords = re.search('%s(.*)%s' % (start, end), link).group(1)
                return coords.split(",")

    def parse_hotel_page(self, response):
        print 'parsing response...'
        item = HotelItem()
        item['name'] = self.extract_data(response,
            "//h1[contains(@class,'heading_name')]/text()")
        item['source_url'] = response.url
        item['address_line'] = self.extract_data(response,
            "//div[@property='address']"
            "//span[@property='streetAddress']/text()")
        item['locality'] = self.extract_data(response,
            "//div[@property='address']"
            "//span[@property='addressLocality']/text()")
        item['state'] = self.extract_data(response,
            "//div[@property='address']"
            "//span[@property='addressRegion']/text()")
        item['postcode'] = self.extract_data(response,
            "//div[@property='address']"
            "//span[@property='postalCode']/text()")
        item['pricerange'] = self.extract_data(response,
            "//span[@property='priceRange']/text()")
        item['room_count'] = self.extract_data(response,
            "//span[@class='tabs_num_rooms']/text()")
        item['alternative_names'] = self.extract_data(response,
            "//dl[@id='AKA']/dd/text()")
        item['amenities'] = self.extract_data(response,
            "//div[@id='AMENITIES_TAB']/div/div/div/ul/li/text()")
        item['traveler_rating'] = self.parse_traveler_rating(response)
        item['rating_summary'] = self.parse_rating_summary(response)
        coordinates = self.parse_coordinates(response)
        item['country'] = self.extract_data(response,
            "//div[@property='address']"
            "//span[@property='addressCountry']/text()")
        if coordinates:
            item['latitude'] = coordinates[0]
            item['longitude'] = coordinates[1]
        stars_string = self.extract_data(response,
            "//img[@property='ratingValue']/@content")
        item['stars'] = stars_string if stars_string else ''
        print item
        yield item
