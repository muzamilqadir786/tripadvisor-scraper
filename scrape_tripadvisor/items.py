import scrapy


class HotelItem(scrapy.Item):
    name = scrapy.Field()
    source_url = scrapy.Field()
    pricerange = scrapy.Field()
    address_line = scrapy.Field()
    locality = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    room_count = scrapy.Field()
    stars = scrapy.Field()
    alternative_names = scrapy.Field()
    amenities = scrapy.Field()
    traveler_rating = scrapy.Field()
    rating_summary = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    country = scrapy.Field()
