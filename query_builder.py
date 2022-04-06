from typing import List, Optional,Union
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
import os
from pathlib import Path
import configparser

config_file = os.path.join(Path(__file__).resolve().parent,"config.ini")
config = configparser.ConfigParser()
config.read(config_file)


class QueryBuilder:
    def __init__(self,driver:webdriver.Chrome):
        self.__queries:List[str] = list()
        assert driver,"driver is required"
        self.__driver:webdriver.Chrome = driver
    
    @property
    def is_debug(self):
        return (config["settings"]["DEBUG"] or '').strip().lower() in ["true",1,'1']

    def reset(self):
        self.__queries = list()
        return self

    # def run(self) -> Union[WebElement,List[WebElement]]:
    def execute(self,element:Optional[WebElement]=None)-> Union[WebElement,List[WebElement]]:
        try:
            
            element = element or self.__driver.find_element(By.CSS_SELECTOR,"body")
            if not element:
                raise Exception("queryBuilder could not retrieve base element")
            query_str = "".join(self.__queries)
            if self.is_debug:print("\n\n query => document.querySelector('body')"+query_str)
            result = self.__driver.execute_script("return arguments[0]"+query_str,element)
        except JavascriptException as e:
            self.reset()
            raise JavascriptException(e)
        self.reset()
        return result


    def elementExists(self,element:Optional[WebElement]=None)->bool:
        try:
            
            element = element or self.__driver.find_element(By.CSS_SELECTOR,"body")
            if not element:
                raise Exception("queryBuilder could not retrieve base element")
            query_str = "".join(self.__queries)
            if self.is_debug:print("\n\n query => document.querySelector('body')"+query_str)
            return bool(self.__driver.execute_script("return arguments[0]"+query_str,element))
        except:
            return False
        

    def getOne(self,selector:str,*args):
        self.__queries.append(f".querySelector('{selector}')")
        for x in args:
            self.__queries.append(f".querySelector('{x}')")
        return self

    def getList(self,selector:str):
        self.__queries.append(f".querySelectorAll('{selector}')")
        return self

    def getOneShadowRoot(self,selector:str,*args):
        self.__queries.append(f".querySelector('{selector}').shadowRoot")
        for x in args:
            self.__queries.append(f".querySelector('{x}').shadowRoot")
        return self


    def action(self,action:str):
        self.__queries.append(action)
        return self


    def exists(self,qs=None,element:Optional[WebElement]=None,*args, **kwargs):
        print("\n\n exists()")
        try:
            qs:QueryBuilder = qs or self
            return bool(qs.execute(element=element,*args, **kwargs))
        except JavascriptException:
            return False

       