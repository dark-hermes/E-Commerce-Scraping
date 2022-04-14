import requests

class Initialization:
    SHOPEE_URL =  "https://shopee.co.id/"
    
    def __init__(self, keyword, limit, is_official):
        self.keyword = keyword
        self.limit = limit
        self.headers = {
            'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            'referrer' : f'{self.SHOPEE_URL}search?keyword={self.keyword}'
        }
        
        if is_official:
            self.seller_type = "ShopeeMall"
        else:
            self.seller_type = "Shopee"
            
        self.is_official = int(is_official)
            
            
class Scrape(Initialization):
    def get_id(self):
        api_id = self.SHOPEE_URL + f"api/v2/search_items/?by=relevancy&keyword={self.keyword}&limit={self.limit}&newest=0&official_mall={self.is_official}&order=desc&page_type=search&version=2"
        self.api_requests = requests.get(api_id, headers=self.headers).json()
        
        self.shop_id, self.item_id = [], []
        
        for item in self.api_requests['items']:
            self.item_id.append(item['itemid'])
            self.shop_id.append(item['shopid'])
            
    def api_crawling(self):
        id_collection = self.get_id()
        item_id = self.item_id
        shop_id = self.shop_id
            
        for i in range(len(item_id)):
            api_item = self.SHOPEE_URL + "/api/v2/item/get?itemid={}&shopid={}".format(item_id[i],shop_id[i])
            api_requests = requests.get(api_item,headers=self.headers).json()
            
            yield api_requests
            
    def get_data(self):
        for request in self.api_crawling():
            item = request['item']
            item_datas = {}
            try:
                for key, value in item.items():
                    item_datas[key] = value
                yield item_datas
            except AttributeError:
                continue
            
    def get_data2(self):
        item_datas = {}
        for request in self.api_crawling():
            item = request['item']
            try:
                for key, value in item.items():
                    try:
                        item_datas[key].append(value)
                    except KeyError:
                        item_datas[key] = [value]
                
            except AttributeError:
                continue
            
        return item_datas
        