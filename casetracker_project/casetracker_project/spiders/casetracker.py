import scrapy


class CasetrackerSpider(scrapy.Spider):
    name = "casetracker"
    allowed_domains = ["casestatusext.com"]
    start_urls = ["https://casestatusext.com/approvals/I-485/IOE-LB"]

    def parse(self, response):
        pass
