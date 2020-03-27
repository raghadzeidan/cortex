import redis
import concurrent.futures as cf
import time


def func(y):
    print("before{num}".format(num=y))
    time.sleep(1)
    print("after{num}".format(num=y))

#with cf.ThreadPoolExecutor(5) as executor:
#    executor.submit(func, 7)
#    executor.submit(func,6)
#    executor.submit(func,5)

executor = cf.ThreadPoolExecutor(5)
executor.submit(func,7)
executor.submit(func,8)
executor.submit(func,9)
