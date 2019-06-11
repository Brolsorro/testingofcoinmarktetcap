from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime as dt
from sys import getsizeof as sizeof

def parse():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'10',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'a215b8c6-e8b9-451b-8300-7581630f3b92',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        time_response=response.elapsed.total_seconds()
        data = json.loads(response.text)
      # print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        # print(e)
        pass

    return data,time_response

def test(time_response=0,last_updates=[],data_inf=[]):
    result_test=[]

    if time_response < 0.5:
        result_test.append(True)
    else:
        result_test.append(False)


    time_now=dt.datetime.now()
    test_last_time=True
    for date in last_updates:
        date=date.split("-")
        date=[int(c) for c in date]
        if date[0]==time_now.year and date[1]==time_now.month and date[2]==time_now.day:
            pass
        else:
            test_last_time=False
    if test_last_time:
        result_test.append(True)
    else:
        result_test.append(False)

    size_data=sizeof(data_inf) # в байтах
    size_data=size_data/1024 # в Кбайтах
    if size_data < 10:
        result_test.append(True)
    else:
        result_test.append(False)

    return result_test,time_response,size_data

def coinmarketcap_fun():
    massive_data=parse()
    last_updates=[c["last_updated"] for c in massive_data[0]["data"]]
    last_updates=[c[:c.find("T")] for c in last_updates]

    result_test_all=test(time_response=massive_data[1],last_updates=last_updates, data_inf=massive_data[0])
    massive_data=massive_data[0]
    return massive_data,result_test_all

if __name__ == '__main__':
    massive_data=coinmarketcap_fun()
    result_test_all=massive_data[1]
    result_test=result_test_all[0]
    print("Информация от тестировании:")
    if result_test[0]:
        print("+ Успешный ответ от ресурса пришел менее чем за 500мс (%sмс)" %(result_test_all[1]))
    else:
        print("- Превышено разрешенное время ответ от ресурса (%sмс). Допустимо не более 500мс." %(result_test_all[1]))

    if result_test[1]:
        print("+ Информация по каждой валюте актуальна")
    else:
        print("- Информация по некоторой валюте не актуальна")

    if result_test[2]:
        print("+ Размер полученного пакета данных не превышает 10кб (%sкб)"%(result_test_all[2]))
    else:
        print("- Размер полученного пакета данных превышает 10кб (%sкб)"%(result_test_all[2]))

    if all(result_test)==True:
        print("Тест выполен успешно!")
    else:
        print("Тест провален! Один или несколько условий не выполнено!")

    massive_data=massive_data[0]
    print("\n")
    print("Данные о 10 тикерах с наибольшим объемом за последние 24 часа.\n")
    print("%s | %s | %s | %s USD"%("Наим. валюты","Симв. обозначение","Послед. обн.","Объем за последние 24 часа"))
    for ticket in massive_data['data']:
        print("%s | %s | %s | %s USD" % (ticket['name'], ticket['symbol'],ticket['last_updated'],int(ticket['quote']['USD']['volume_24h'])))
