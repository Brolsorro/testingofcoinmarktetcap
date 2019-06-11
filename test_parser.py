from coinmarketinfo import coinmarketcap_fun
import datetime as dt
import time
if __name__ == '__main__':

    results_of_test=[]
    respone_times=[]
    time_start=dt.datetime.now()
    for i in range(8):
        result_last_test=coinmarketcap_fun()
        respone_times.append(result_last_test[1][1])
        result_last_test=result_last_test[1][0]
        results_of_test.append(result_last_test[0])
        results_of_test.append(result_last_test[1])
        results_of_test.append(result_last_test[2])
    status_test_2=[]
    if all(results_of_test)==True:
        print(" + Все запущенные тесты выполнились успешно")
        status_test_2.append(True)
    else:
        print(" - НЕ все запущенные тесты выполнились успешно")
        status_test_2.append(False)
    time_stop=dt.datetime.now()-time_start
    rps=sum(respone_times)/8

    if rps>5:
        print(" + rps > 5  (%s)"%(rps))
        status_test_2.append(True)
    else:
        print(" - rps < 5  (%s)"%(rps))
        status_test_2.append(False)

    latency_time=[(c/100)*80 for c in respone_times]

    if all(latency_time)<0.450:
        print(" + 80% latency < 450мс")
        status_test_2.append(True)
    else:
        print(" - 80% latency < 450мс")
        status_test_2.append(False)

    if all(status_test_2)==True:
        print("Тест №2 над тестом №1 прошел успешно!")
    else:
        print("Тест №2 над тестом №1 провален!")
