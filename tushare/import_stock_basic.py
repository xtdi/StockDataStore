import tushare as ts
import time

def import_basic_info():

    token = "027a261a949c5b5d8b631061961020ac7ad999c66e9d88baf23428fd"
    tushare_pro = ts.pro_api(token)
    data_list = tushare_pro.query("stock_basic", exchange="", list_status="L", fields="ts_code,symbol,name,area,industry,list_date")
    print()

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
