#!/usr/bin/env python
#coding=utf-8

#1.异步:多任务，多个任务之间执行没有先后顺序，可以同时运行，执行的先后顺序不会有什么影响，存在的多条运行主线
#2.同步:多任务，多个任务之间执行的时候要求有先后顺序，必须一个先执行完成之后，另一个才能继续执行，只有一个主线
#3.阻塞：从调用者的角度出发，如果在调用的时候，被卡住，不能再继续向下运行，需要等待，就说是阻塞
#4.非阻塞:从调用者的角度出发， 如果在调用的时候，没有被卡住，能够继续向下运行，无需等待，就说是非阻塞

from multiprocessing import Pool, Process
from time import sleep
import os
import datetime

def f(x):
  starttime = datetime.datetime.now()
  print 'Run: %s --- %s ' % (os.getpid(), x)
  sleep(10)
  endtime = datetime.datetime.now()
  print 'End: %s --- %s ' % (os.getpid(), (endtime - starttime).microseconds)
  return x  
  
def main():
  start = datetime.datetime.now()
  pool = Pool(3)
 
  #异步非阻塞---14
  #result = [] 
  for i in range(3):
    #result.append(pool.apply_async(f, (i,)))
    res = pool.apply_async(f, (i,))
    print res.get()

  #for res in result:
  #  print res.get()

  #  result = pool.apply_async(f, (i,))
  #if result.successful():
  #  print 'successful'

  pool.close()
  pool.join()

  #异步阻塞,自带join,close---13
  #result = pool.map(f, range(3))
  

  #同步阻塞---23
  #for i in range(3):
  #  result = pool.apply(f, (i,))
  
  #for i in range(3):
  #  p = Process(target=f, args=(i,))
  #  p.start()
  #  p.join()
  
  end = datetime.datetime.now()
  print "The parent process: ", (end - start).microseconds


if __name__ == "__main__":
  main()

