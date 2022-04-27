from datetime import timedelta
from time import sleep
from typing import Optional
from threading import Timer




class Tracker:
    
    def __init__(self,function:callable,time:timedelta=timedelta(hours=2)):
        self.__time = time.total_seconds()
        self.__task:Optional[Timer] = None
        self.__function:callable = function

    @property
    def get_time(self) -> float:
        return self.__time

    @property
    def restart(self):
        return self.__function

    @restart.setter
    def restart(self,value):
        assert callable(value),"value must be callable"
        self.__function = value
        return self

    @property
    def is_alive(self):
        return bool(self.__task and self.__task.is_alive())
    	
    def reset(self,seconds: Optional[float] = 0, days: Optional[float] = 0, microseconds: Optional[float] = 0, milliseconds: Optional[float] = 0, minutes: Optional[float] = 0, hours: Optional[float] = 0, weeks: Optional[float] = 0,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().reset()")
        self.start(days = days, seconds = seconds, microseconds = microseconds, milliseconds = milliseconds, minutes = minutes, hours = hours , weeks=weeks,*args, **kwargs)
        return self

    def wait(self,seconds: Optional[float] = 0, days: Optional[float] = 0, microseconds: Optional[float] = 0, milliseconds: Optional[float] = 0, minutes: Optional[float] = 0, hours: Optional[float] = 0, weeks: Optional[float] = 0,*args, **kwargs):
        _time:float = timedelta(days = days, seconds = seconds, microseconds = microseconds, milliseconds = milliseconds, minutes = minutes, hours = hours , weeks=weeks,*args, **kwargs).total_seconds()
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}() waiting for "+str(_time)," seconds")
        sleep(_time)

    def start(self,seconds: Optional[float] = 0, days: Optional[float] = 0, microseconds: Optional[float] = 0, milliseconds: Optional[float] = 0, minutes: Optional[float] = 0, hours: Optional[float] = 0, weeks: Optional[float] = 0,*args, **kwargs):
        """start is called if after "sec" second this method is not called"""
        _time:float = timedelta(days = days, seconds = seconds, microseconds = microseconds, milliseconds = milliseconds, minutes = minutes, hours = hours , weeks=weeks,*args, **kwargs).total_seconds()
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}() timer set for ",_time or self.__time," second(s)")
        assert self.__function,"restart function is not provided"
        self.__time = _time or self.__time
        self.stop()
        self.__task = None
        self.__task = Timer(self.__time,self.__function)
        self.__task.setDaemon(True)
        self.__task.start()
        return self

    def stop(self,*args, **kwargs):
        if self.__task and self.__task.is_alive():
            self.__task.cancel()
            sleep(0.2)
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().stop(is_alice={self.__task and self.__task.is_alive()})")
        return self

    @property
    def task(self):
        return self.__task

    def check_conditions(self,*conditions,**kwargs):
        is_or = kwargs.get("is_or",False)
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().check_conditions(is_or={is_or},{conditions})")
        """_summary_

        Args:
            is_or (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        res = []
        for con in conditions:
            if callable(con):
                res.append(bool(con()))
            elif type(con)==list:
                res.append(self.check_conditions(*con))
            elif type(con)==dict:
                res.append(self.check_conditions(*con.values()))
            else:
                res.append(bool(con))
        # print(f"\n\n [{self.__class__}]{self.__class__.__name__}(). res ",res)
        if not res:return 
        return any(res)  if is_or else all(res)


    def wait_til_condition(self,function:Optional[callable]=None,conditions=[],or_conditions=[],delay_in_seconds:Optional[float]=10,max_loop:Optional[int]=None,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().loop_til_condition()")
        # print(f"\n\n loop_til_condition(function={function},conditions={conditions},or_conditions={or_conditions},delay_in_seconds={delay_in_seconds}),{args},{kwargs}")
        """_summary_
        
        Args:
            function (Optional[callable], optional): _description_. Defaults to None.
            conditions (list, optional): _description_. Defaults to [].
            or_conditions (list, optional): _description_. Defaults to [].
            delay_in_seconds (Optional[float], optional): _description_. Defaults to 0.
        """
        stop = self.check_conditions(*conditions) or self.check_conditions(*or_conditions,is_or=True)
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}(). stop = ",stop)
        count = 0
        while not stop:
            if function:
                function()
            self.wait(seconds=delay_in_seconds)
            stop = self.check_conditions(*conditions) or self.check_conditions(*or_conditions,is_or=True)
            print("stop = ",stop)
            count +=1
            if max_loop and max_loop==count:
                break




# if __name__ == '__main__':
#     main()
    
