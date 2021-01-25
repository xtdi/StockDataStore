import tushare as ts
import time
import datetime
from mariadb.mariadb_manager import MariadbManager
from entity.stock_info_entity import StockInfoEntity


def init_stock_basic_info():

    token = "027a261a949c5b5d8b631061961020ac7ad999c66e9d88baf23428fd"
    query_field_list = ["ts_code", "symbol", "name", "area", "industry", "fullname", "enname", "market",
                         "exchange", "curr_type", "list_status", "list_date", "delist_date", "is_hs"]
    query_field_list_str = ','.join(query_field_list)

    table_field_list = ["ts_code", "stock_code", "stock_name", "area", "industry", "stock_fullname", "english_name",
                         "market_type",  "exchange_code", "currency_type", "list_status", "list_date", "delist_date",
                         "is_hs"]
    table_field_list_str = ','.join(table_field_list)

    mariadb_manager = MariadbManager("127.0.0.1", 3306, "stockdata", "root", "pmo@2016",  charset="utf8mb4")
    mariadb_manager.open_connect()
    insert_sql_stmt = "INSERT INTO stock_info (" + table_field_list_str + ")VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    tablefield_queryfield_dict = get_tablefield_queryfield_dict()

    tushare_pro = ts.pro_api(token)
    data_frame = tushare_pro.query("stock_basic", exchange="", list_status="", fields=query_field_list_str)
    column_name_list = data_frame.columns.tolist()
    if len(query_field_list) != len(table_field_list):
        print("查询返回的列数与请求的列数不一致，请检查！")
        return
    data_list = []
    for each_row_tuple in data_frame.iterrows():
        temp_row_no = each_row_tuple[0]
        each_row_series = each_row_tuple[1]
        row_value_tuple = ()
        for i in range(len(table_field_list)):
            temp_table_field = table_field_list[i]
            temp_query_field = tablefield_queryfield_dict[temp_table_field]
            temp_value_str = each_row_series[temp_query_field]
            if temp_value_str is None:
                temp_tuple = (None, )
                row_value_tuple = row_value_tuple + temp_tuple
                continue
            if temp_table_field == "list_date":
                temp_list_date_str = ""

                if len(temp_value_str.strip()) == 0:
                    temp_list_date_str = "null"
                else:
                    temp_list_date_str = "str_to_date('" + temp_value_str.strip() + "','%Y%m%d')"
                temp_list_date_tuple = (datetime.date.strftime(temp_value_str.strip(), '%Y%m%d'), )
                row_value_tuple = row_value_tuple + temp_list_date_tuple

            elif temp_table_field == "delist_date":
                temp_delist_date_str = ""
                if len(temp_value_str.strip()) == 0:
                    temp_delist_date_str = "null"
                else:
                    temp_delist_date_str = "str_to_date('" + temp_value_str.strip() + "','%Y%m%d')"
                    # datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                temp_delist_date_tuple = (temp_delist_date_str, )
                row_value_tuple = row_value_tuple + temp_delist_date_tuple
            else:
                temp_value_tuple = (each_row_series[temp_query_field],)
                row_value_tuple = row_value_tuple + temp_value_tuple
        data_list.append(row_value_tuple)
        print(temp_row_no)
        batch_insert_data(mariadb_manager.connect, insert_sql_stmt, data_list)
        break
    print()


def get_tablefield_queryfield_dict():
    field_name_dict = {}
    field_name_dict["ts_code"] = "ts_code"
    field_name_dict["stock_code"] = "symbol"
    field_name_dict["stock_name"] = "name"
    field_name_dict["area"] = "area"
    field_name_dict["industry"] = "industry"
    field_name_dict["stock_fullname"] = "fullname"
    field_name_dict["english_name"] = "enname"
    field_name_dict["market_type"] = "market"
    field_name_dict["exchange_code"] = "exchange"
    field_name_dict["currency_type"] = "curr_type"
    field_name_dict["list_status"] = "list_status"
    field_name_dict["list_date"] = "list_date"
    field_name_dict["delist_date"] = "delist_date"
    field_name_dict["is_hs"] = "is_hs"
    return field_name_dict


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
        init_stock_basic_info()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':

    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('Beginning ! Begin:' + start_time)
    main()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('\nEnd:' + end_time)
