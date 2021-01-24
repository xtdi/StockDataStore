import tushare as ts
import time
from mariadb.mariadb_manager import MariadbManager
from entity.stock_info_entity import StockInfoEntity


def import_basic_info():

    token = "027a261a949c5b5d8b631061961020ac7ad999c66e9d88baf23428fd"
    tushare_pro = ts.pro_api(token)
    out_fields_str = "ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs"
    data_frame = tushare_pro.query("stock_basic", exchange="", list_status="", fields=out_fields_str)
    for each_row_tuple in data_frame.iterrows():
        temp_row_no = each_row_tuple[0]
        each_row_series = each_row_tuple[1]
        field_dict = to_stock_info_entity_dict(get_field_name_dict(), each_row_series)
        stock_info_entity = StockInfoEntity(field_dict)
        temp_ts_code = each_row_series["ts_code"]
        print(temp_row_no)
    print()
    mariadb_manager = MariadbManager("127.0.0.1", 3306, "privacydata", "root", "pmo@2016",  charset="utf8mb4")
    mariadb_manager.open_connect()
    insert_sql_stmt = "INSERT INTO stock_info (phone, uid)VALUES(%s,%s)"


def get_field_name_dict():
    field_name_dict = {}
    field_name_dict["ts_code"] = "ts_code"
    field_name_dict["symbol"] = "stock_code"
    field_name_dict["name"] = "stock_name"
    field_name_dict["area"] = "area"
    field_name_dict["industry"] = "industry"
    field_name_dict["fullname"] = "stock_fullname"
    field_name_dict["enname"] = "english_name"
    field_name_dict["market"] = "market_type"
    field_name_dict["exchange"] = "exchange_code"
    field_name_dict["curr_type"] = "currency_type"
    field_name_dict["list_status"] = "list_status"
    field_name_dict["list_date"] = "list_date"
    field_name_dict["delist_date"] = "delist_date"
    field_name_dict["is_hs"] = "is_hs"
    return field_name_dict


def to_stock_info_entity_dict(field_name_dict, fields_series):
    result_dict = {}
    query_key_array = fields_series.keys().array
    for i in range(len(query_key_array)):
        query_key = query_key_array[i]
        field_key = field_name_dict[query_key]
        result_dict[field_key] = fields_series[query_key]
    return result_dict


def batch_insert_data(mariadb_conn, sql_stmt, values_list):

    begin_time = time.time()
    table_cursor = mariadb_conn.cursor()
    total_count = 0
    try:
        total_count = table_cursor.executemany(sql_stmt, values_list)
        mariadb_conn.commit()
    except Exception as ex:
        print(ex)
        mariadb_conn.rollback()
    table_cursor.close()
    end_time = time.time()
    spend_time = end_time-begin_time
    print("本次插入数据%d条" % total_count+"  共计花费时间:%s秒" % format(spend_time, '0.2f'))
    return total_count


def main():

    try:
        import_basic_info()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':

    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('Beginning ! Begin:' + start_time)
    main()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('\nEnd:' + end_time)
