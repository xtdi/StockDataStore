import datetime


class StockInfoEntity(object):
    # 初始化方法
    def __init__(self, fileds_dict):

        # filed_keys_list = fileds_dict.keys().tolist()

        self.__ts_code = fileds_dict.get("ts_code")
        self.__stock_code = fileds_dict.get("stock_code")
        self.__stock_name = fileds_dict.get("stock_name")
        self.__area = fileds_dict.get("area")
        self.__industry = fileds_dict.get("industry")
        self.__stock_fullname = fileds_dict.get("stock_fullname")
        self.__english_name = fileds_dict.get("english_name")
        self.__market_type = fileds_dict.get("market_type")
        self.__exchange_code = fileds_dict.get("exchange_code")
        self.__currency_type = fileds_dict.get("currency_type")
        self.__list_status = fileds_dict.get("list_status")
        list_date_str = fileds_dict.get("list_date")
        delist_date_str = fileds_dict.get("delist_date")

        if list_date_str is None:
            self.__list_date = None
        else:
            self.__list_date = datetime.datetime.strptime(list_date_str, "%Y%m%d")

        if delist_date_str is None:
            self.__delist_date = None
        else:
            self.__delist_date = datetime.datetime.strptime(delist_date_str, "%Y%m%d")
        self.__is_hs = fileds_dict.get("is_hs")

    # getter
    @property
    def ts_code(self):
        return self.__ts_code

    # settter
    @ts_code.setter
    def ts_code(self, ts_code):
        self.__ts_code = ts_code

    # getter
    @property
    def stock_code(self):
        return self.__stock_code

    # settter
    @stock_code.setter
    def stock_code(self, stock_code):
        self.__stock_code = stock_code

    # getter
    @property
    def stock_name(self):
        return self.__stock_name

    # settter
    @stock_name.setter
    def stock_name(self, stock_name):
        self.__stock_name = stock_name

    # getter
    @property
    def area(self):
        return self.__area

    # settter
    @area.setter
    def area(self, area):
        self.__area = area

    # getter
    @property
    def industry(self):
        return self.__industry

    # settter
    @industry.setter
    def industry(self, industry):
        self.__industry = industry

    # getter
    @property
    def stock_fullname(self):
        return self.__stock_fullname

    # settter
    @stock_fullname.setter
    def stock_fullname(self, stock_fullname):
        self.__stock_fullname = stock_fullname

    # getter
    @property
    def english_name(self):
        return self.__english_name

    # settter
    @english_name.setter
    def english_name(self, english_name):
        self.__english_name = english_name

    # getter
    @property
    def market_type(self):
        return self.__market_type

    # settter
    @market_type.setter
    def market_type(self, market_type):
        self.__market_type = market_type

    # getter
    @property
    def exchange_code(self):
        return self.__exchange_code

    # settter
    @exchange_code.setter
    def exchange_code(self, exchange_code):
        self.__exchange_code = exchange_code

    # getter
    @property
    def currency_type(self):
        return self.__currency_type

    # settter
    @currency_type.setter
    def currency_type(self, currency_type):
        self.__currency_type = currency_type


    # getter
    @property
    def list_status(self):
        return self.__list_status

    # settter
    @list_status.setter
    def list_status(self, list_status):
        self.__list_status = list_status

    # getter
    @property
    def is_hs(self):
        return self.__is_hs

    # settter
    @is_hs.setter
    def is_hs(self, is_hs):
        self.__is_hs = is_hs
