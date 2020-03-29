import redis
import concurrent.futures as cf
import time
from utils.connection import Connection

#
#
#def func(y,z):
#    print("before{num}".format(num=y))
#    time.sleep(1)
#    print("after{num}".format(num=z))
#
##with cf.ThreadPoolExecutor(5) as executor:
##    executor.submit(func, 7)
##    executor.submit(func,6)
##    executor.submit(func,5)
#
#executor = cf.ThreadPoolExecutor(5)
#executor.submit(func,7,77)
#executor.submit(func,8,88)
#executor.submit(func,9,99)
