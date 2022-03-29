from datetime import datetime, timedelta
from typing import List, Optional
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

import os
from time import sleep
import re
from query_builder import QueryBuilder
from utils.helpers import Tracker
from threading import Timer
from selenium.common.exceptions import TimeoutException

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


"""
downgrade info
https://browserhow.com/how-to-downgrade-and-install-older-version-of-chrome/#step-4-disable-chrome-auto-updates


updater path
C:\\Users\\HP\AppData\\Local\\Google\\Update

"""


# room_link = 'https://wolf.live/g/18336134'





url = 'https://wolf.live/'
chrome_options = Options()
chrome_options.add_experimental_option('w3c', True)
absolute_path = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(absolute_path, '../chromedriver')

# chrome_options.add_argument("--start-maximized")  # To open chrome in full screen

# edge configuration
edgedriver_path = os.path.join(absolute_path, '../msedgedriver.exe')
firefoxdriver_path = os.path.join(absolute_path, '../geckodriver.exe')






class WebDriver:
    selectors = []
    def __init__(self, username, password,room_link = 'https://wolf.live/g/18900545'):
        self.username = username
        self.password = password
        self.room_link = room_link
        self.task = None

        

        self.tracker = Tracker(self.restart,timedelta(hours=2))
        sleep(2)
        # self.update_driver()
        


    def update_driver(self):
        try:
            self.driver.quit()
        except:
            pass
        
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_path)
        # self.driver = webdriver.Edge(executable_path=edgedriver_path)
        # self.driver = webdriver.Firefox(executable_path=firefoxdriver_path)
        self.driver.set_page_load_timeout(80)
        self.is_login = False
        

        try:
            for retry in range(7):
                try:
                    self.login()
                    break
                except TimeoutException:
                    if retry > 5:
                        raise Exception("maximum retry has been reached")
                    self.driver.refresh()
            self.is_login = True
        except Exception as e:
            print("\n\n error ",e)
            self.driver.quit()
            raise Exception("couldn't login")

    @property
    def qs(self):
        return QueryBuilder(self.driver)

    def check_and_remove_install_app_model(self):
        data = []

			
    def restart(self,*args, **kwargs):
        print("\n\n restart()")
        raise NotImplementedError

    def restart_if_stalk(self,sec=60.0):
        print("\n\n restart_if_stalk()")
        """start is called if after "sec" second this method is not called"""
        print("\n\n timer set for ",sec," second(s)")
        if self.task:
            self.task.cancel()
            self.task = None
        self.task = Timer(sec,self.restart)
        self.task.setDaemon(True)
        self.task.start()
        

    def check_autoplay(self,cmd,config_section):
        print("\n\n check_autoplay()")
        self.send_msg(cmd)
        for _ in range(20):
            if self.is_bot():
                break
            sleep(0.3)
        text = self.get_last_bot_msg()
        if config[config_section.title()]['autoplay'].upper() not in text:
            self.toggle_autoplay(cmd)
            


    def toggle_autoplay(self,cmd):
        print("\n\n toggle_autoplay()")
        self.send_msg(cmd)

        
    def expand_shadow_element(self, element):
        print("\n\n expand_shadow_element()")
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot',element)
        return shadow_root

    def login(self):
        print("\n\n login()")
        print(datetime.now())
        self.driver.get(self.room_link)
        print(datetime.now())
        self.driver.implicitly_wait(20)
        print(datetime.now())
        sleep(6)
        
        print(datetime.now())
        if self.exist([
            "palringo-install-android:",
            "#androidDismissButton"
        ]):
            try:
                self.expand_all_v2([
                    "palringo-install-android:",
                    "#androidDismissButton"
                ]).click()
            except:
                pass
            print("\n\n clicked androidDismissButton")

        sleep(10)
        print(datetime.now())
        print("\n\n am here")
        self.expand_all_v2([
            "route-layout:sidebar-layout",
            "palringo-sidebar:palringo-sidebar-profile",
            "#status"
        ]).click()

        print(datetime.now())
        self.driver.implicitly_wait(20)
        
        
        self.expand_all_v2([
            "login-dialog:",
            "#palringo-login"
        ]).click()
        self.driver.implicitly_wait(20)
        sleep(4)
        print(datetime.now())
        
        self.expand_all_v2([
            "login-dialog:",
            "#email"
        ]).send_keys(self.username)
        sleep(4)
        print(datetime.now())
        
        self.expand_all_v2([
            "login-dialog:",
            "#password"
        ]).send_keys(self.password)
        print(datetime.now())
        sleep(4)
        
        self.expand_all_v2([
            "login-dialog:",
            "#sign-in",
        ]).click()

        print(datetime.now())

    
    
    def send_msg(self, msg):
        print("\n\n send_msg()")
        self.driver.implicitly_wait(20)

        # Enter Msg
       
        self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "app-routes",
            "group-chat-page",
            "palringo-chat",
            "palringo-chat-input",
            "iron-autogrow-textarea",
        ).getOne("textarea").execute().send_keys(msg.strip())
        
        self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout",
            "paper-drawer-panel",
            "app-routes",
            "group-chat-page",
            "palringo-chat",
            "palringo-chat-input"
        ).getOne("send-button").execute().click()

    def get_latest_bot_msgs(self,private=False):
        print("\n\n get_latest_bot_msgs()")
        return [x for x in self.get_latest_msgs(private=private).execute() if x.get_attribute("is-bot")=='']
        

    def get_latest_user_msgs(self):
        print("\n\n get_latest_user_msgs()")
        elements = self.get_latest_msgs().execute()
        print("\n\n here am i")
        return [x for x in elements if x.get_attribute("is-bot")!='']

    def get_latest_msgs(self,private=False):
        print("\n\n get_latest_msgs()")
        self.driver.implicitly_wait(20)
        d = "user" if private else "group"
        return self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "app-routes",
            f"{d}-chat-page",
            "palringo-chat"
        ).getOne("#chat-container").getList("palringo-chat-message")

    def get_last_msg(self,index=-1):
        print("\n\n get_last_msg()")
        """
        function get the latestest message in test form
        """
        length = self.get_latest_msgs().action(".length").execute() -1 + index
        try:
            return self.get_latest_msgs().action(f"[{length}].shadowRoot").getOne("palringo-chat-message-text").action(".text").execute()
        except:
            return ''

    def is_bot(self):
        print("\n\n is_bot()")
        """return true if last message is from a bot"""
        return self.get_last_element().get_attribute("is-bot")==''



    def get_last_bot_msg(self,index=-1,private=False):
        print("\n\n get_last_bot_msg()")
        """
        function get the latestest message in test form
        """
        try:
            return self.qs.action(".shadowRoot").getOneShadowRoot('palringo-chat-message-text').action(".text").execute(self.get_latest_bot_msgs(private=private)[index])
            # return self.expand_shadow_element(self.get_latest_bot_msgs()[index]).find_element_by_css_selector('palringo-chat-message-text').text
        except:
            return ''




    def get_last_user_msg(self,index=-1):
        print("\n\n get_last_user_msg()")
        """
        function get the latestest message in test form
        """
        try:
            elements = self.get_latest_user_msgs()
            if not elements:
                return ""
            element = elements[index]
            return self.qs.action(".shadowRoot").getOneShadowRoot("palringo-chat-message-text").action(".text").execute(element)
            # return self.expand_shadow_element().find_element_by_css_selector('palringo-chat-message-text').text
        except Exception as e:
            print("\n\n erro while getting user message ",e)
            return ''
        




    def get_latest_pm(self):
        print("\n\n get_latest_pm()")
        self.driver.implicitly_wait (20)
        return self.qs.getOneShadowRoot(
            'route-layout',
            'sidebar-layout'
        ).getOne('paper-drawer-panel').getOneShadowRoot(
            'app-routes',
            'user-chat-page',
            'palringo-chat',
        ).getOne('#chat-container').getList("palringo-chat-message")

    def change_inbox(self):
        print("\n\n change_inbox()")
        self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "palringo-sidebar",
            "paper-tabs"
        ).getOne("paper-tab[title='Chats']").action(".click()").execute()

    def close(self):
        print("\n\n close()")
        self.driver.quit()


    def is_stop(self):
        print("\n\n is_stop()")
        return bool(re.findall(r'!stop',self.get_last_user_msg() or '',re.I))

    
    def transfrom(self,selector:str):
        print("\n\n transfrom()")
        if ":" in selector:
            return "".join([f".querySelector('{x}').shadowRoot" for x in selector.split(":") if x])
        else:
            return f".querySelector('{selector}')"
    
    def expand_all_v2(self,data:list,element:Optional[WebElement]=None):
        print("\n\n expand_all_v2()")
        sleep(2)
        query:List[str] = map(self.transfrom,data)
        query_str = "".join(query)
        if not element:
            element = self.driver.find_element(By.CSS_SELECTOR,"body")
        return self.driver.execute_script("return arguments[0]"+query_str, element)


    def exist(self,selectors):
        print("\n\n exist()")
        try:
            return bool(self.expand_all_v2(selectors))
        except:
            return False
                

    def expand_all(self,data:list):
        print("\n\n expand_all()")
        sleep(2)
        self.driver.implicitly_wait(10)
        result = self.driver.find_element_by_css_selector(data[0])
        for x in data[1:]:
            self.driver.implicitly_wait(10)

            result = self.expand_shadow_element(result)
            result = result.find_element_by_css_selector(x)
        return result
    

    def element_exists(self,selectors=list()):
        print("\n\n element_exists()")
        return self.exist(selectors)


    def get_last_element(self,index=-1):
        print("\n\n get_last_element()")
        """
        function get the latestest message in test form
        """
        length = self.get_latest_msgs().action(".length").execute() -1 + index
        return self.get_latest_msgs().action(f"[{length}]").execute()






#%%




if __name__ == '__main__':
   pass






