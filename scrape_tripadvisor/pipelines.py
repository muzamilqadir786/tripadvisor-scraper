from scrapy.exceptions import DropItem

class HotelItemPipeline(object):
    def process_item(self, item, spider):
        if item['country'] != "" and item['country'] != "United States": 
            raise DropItem("Drop hotel %s from %s" % 
                (item['name'], item['country']))
        return item

