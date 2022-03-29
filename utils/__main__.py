import logging
import os
import sys
import time



logging.basicConfig(level=logging.DEBUG,filename=os.path.join(os.getcwd(),'../log.txt'),\
    format="[%(asctime)s]|[%(levelname)s]:[func-> %(func)s t=%(time_taken)ssec]:[args-> %(_args)s | kwargs-> %(_kwargs)s]:[%(message)s]:[file -> %(my_module)s]:"
    )





def logger(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        values = function(*args, **kwargs)
        extra={
            "func":function.__name__ or '',
            "my_module":function.__module__ or '',
            "_args":args or (),
            "_kwargs":kwargs or {},
            "time_taken":time.time()-start,
        }
        try:
            logging.log(kwargs.get("level",logging.INFO),kwargs.get("message",''),extra=extra)
        except Exception as e:
            print("from log",e)
        
        return values
    return wrapper

def log(level:int,message:str=str(),name:str=str(),module:str=str())-> None:
    extra={
        "func":name,
        "my_module":module,
        "_args":[],
        "_kwargs":{},
        "time_taken":0.0,
    }
    logging.log(level,message,extra=extra)