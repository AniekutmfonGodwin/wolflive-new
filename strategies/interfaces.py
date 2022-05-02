from abc import ABC,abstractmethod
from typing import List, Optional
from selenium import webdriver
from query_builder import QueryBuilder
from utils.helpers import Tracker
from selenium.webdriver.remote.webelement import WebElement



class BaseWolfliveStrategyInterface(ABC):
    selectors:List[str]=list()
    __tracker:Tracker
    driver:webdriver.Chrome
    autoplay:bool = bool()

    @abstractmethod
    def goto_group(self):
        ...

    @abstractmethod
    def goto_private(self):
        ...

    @abstractmethod
    def restart(self):
        ...

    

    @property    
    @abstractmethod
    def tracker(self)->Tracker:
        ...

    @property    
    @abstractmethod
    def qs(self)->QueryBuilder:
        ...

    
    @abstractmethod
    def close(self)->None:
        ...


class GetMessageStrategyInterface(ABC):

    @abstractmethod
    def get_last_msg(self,index=-1)->str:
        ...

    @abstractmethod
    def get_latest_msgs(self,private=False)->QueryBuilder:
        ...

    @abstractmethod
    def get_latest_user_msgs(self)->List[WebElement]:
        ...

    @abstractmethod
    def get_latest_bot_msgs(self,private=False)->List[WebElement]:
        ...

    @abstractmethod
    def get_last_message_private(self)->str:
        ...

    @abstractmethod
    def get_lastest_messages_private(self)->QueryBuilder:
        ...

    @abstractmethod
    def get_latest_msgs(self, private: bool = False)->QueryBuilder:
        ...

    @abstractmethod
    def get_last_bot_msg(self,index=-1,private=False)->str:
        ...



    @abstractmethod
    def get_last_user_msg(self,index=-1)->str:
        ...
        



    @abstractmethod
    def get_latest_pm(self)->QueryBuilder:
        ...

    @abstractmethod
    def get_last_element(self,index=-1)->WebElement:
        ...


class SendMessageStrategyInterface(ABC):
    
    @abstractmethod
    def send_msg(self, msg:str,private:bool=False):
        ...

    @abstractmethod
    def send_message_private(self, msg):
        ...

    @abstractmethod
    def send_message_group(self, msg):
        ...

    @abstractmethod
    def wait_for_bot_group(self,*,count:int=100,delay_in_second:float=0.5)->str:
        ...

    @abstractmethod
    def wait_for_message_group(self,text:str,count:int=100,delay_in_second:float=0.5)->str:
        ...

    
            

class CheckStrategyInterface(ABC):

    @abstractmethod
    def is_bot(self)->bool:
        ...

    @abstractmethod
    def is_stop(self)->bool:
        ...

    @abstractmethod
    def message_box_exists(self,private:Optional[bool]=False)->bool:
        ...

    @property
    @abstractmethod
    def is_debug(self)->bool:
        ...

    @property
    @abstractmethod
    def is_login(self)->bool:
        ...

    


class LoginStrategyInterface(ABC):
    username:str
    password:str
    private_url:Optional[str] = None
    room_link:Optional[str] = None
    
    @abstractmethod
    def set_driver(self):
        ...

    @abstractmethod
    def update_driver(self):
        ...

    @abstractmethod
    def login(self):
        ...