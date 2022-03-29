from dataclasses import dataclass
from datetime import datetime, timedelta
import os
import re
from typing import List, Optional
from query_builder import QueryBuilder
from selenium import webdriver
from strategies.interfaces import BaseWolfliveStrategyInterface, CheckStrategyInterface, GetMessageStrategyInterface, SendMessageStrategyInterface
from utils.helpers import Tracker
from selenium.common.exceptions import TimeoutException,JavascriptException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import configparser
config = configparser.ConfigParser()
config.read('config.ini')



url = 'https://wolf.live/'
chrome_options = Options()
chrome_options.add_experimental_option('w3c', True)
absolute_path = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(absolute_path, '../chromedriver')







class BaseWolfliveStrategy:
    selectors:List[str]=list()
    driver:webdriver.Chrome
    

    def goto_group(self):
        print("\n\n goto_group()")
        self.driver.switch_to.window(self.driver.window_handles[0])
        

    def goto_private(self):
        print("\n\n goto_private()")
        private_url = getattr(self,"private_url",None)
        if private_url and len(self.driver.window_handles) <2:
            self.driver.execute_script(f"window.open('{private_url}');")
            self.tracker.wait(seconds=10)
        self.driver.switch_to.window(self.driver.window_handles[1])


    def restart(self):
        ...

    @property
    def tracker(self):
        if not getattr(self,"__tracker",None):
            self.__tracker = Tracker(self.restart,timedelta(hours=2))
        return self.__tracker

    @property
    def qs(self):
        return QueryBuilder(self.driver)

    def close(self):
        print("\n\n close()")
        self.driver.quit()




class GetMessageStrategy(BaseWolfliveStrategyInterface):
    """responsible for getting input

    Args:
        BaseWolfliveStrategyInterface (_type_): _description_
    """
    def get_last_msg(self,index=-1):
        print("\n\n get_last_msg()")
        """
        function get the latestest message in test form
        """
        try:
            elements = self.get_latest_msgs().execute()
            element = elements[index]
            return self.qs.action(".shadowRoot").getOne("palringo-chat-message-text").action(".text").execute(element)
        except:
            print("\n\n could not retrieve last element")
            return ''

    def get_latest_msgs(self,private=False):
        print("\n\n get_latest_msgs()")
        self.goto_private() if private else self.goto_group()
        d = "user" if private else "group"
        return self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "app-routes",
            f"{d}-chat-page",
            "palringo-chat"
        ).getOne("#chat-container").getList("palringo-chat-message")

    def get_latest_user_msgs(self):
        print("\n\n get_latest_user_msgs()")
        elements = self.get_latest_msgs().execute()
        print("\n\n here am i")
        return [x for x in elements if x.get_attribute("is-bot")!='']

    def get_latest_bot_msgs(self,private=False)-> List[WebElement]:
        print(f"\n\n get_latest_bot_msgs(private={private})")
        return [x for x in self.get_latest_msgs(private=private).execute() if x.get_attribute("is-bot")=='']

    def get_last_message_private(self):
        print("\n\n get_last_message_private()")
        self.goto_private()
        self.driver.implicitly_wait(20)
        elements = self.get_lastest_messages_private().execute()
        if not elements:
            return ''
        return elements[-1].text

    def get_lastest_messages_private(self):
        print("\n\n get_lastest_messages_private()")
        self.goto_private()
        return self.get_latest_msgs(private=True)

    def get_latest_msgs(self, private: bool = False):
        print(f"\n\n get_latest_msgs(private = {private})")
        self.goto_private() if private else self.goto_group()
        self.driver.implicitly_wait(20)
        d = "user" if private else "group"
        return self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne(
            "paper-drawer-panel"
        ).getOneShadowRoot(
            "app-routes",
            f"{d}-chat-page",
            "palringo-chat"
        ).getOne(
            "#chat-container"
        ).getList("palringo-chat-message")


    def get_last_bot_msg(self,index=-1,private=False)->str:
        print("\n\n get_last_bot_msg()")
        """
        function get the latestest message in test form
        """
        self.goto_private() if private else self.goto_group()
        try:
            return self.qs.action(".shadowRoot").getOneShadowRoot('palringo-chat-message-text').action(".text").execute(self.get_latest_bot_msgs(private=private)[index])
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
            return self.qs.action(".shadowRoot")\
                .getOneShadowRoot("palringo-chat-message-text")\
                    .action(".text").execute(element)
        except Exception as e:
            print("\n\n error while getting user message ",e)
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

    def get_last_element(self,index=-1):
        print("\n\n get_last_element()")
        """
        function get the latestest message in test form
        """
        elements = self.get_latest_msgs().execute()
        assert elements," could not find last element when get_last_element() was called "
        return elements[index]

        




class CheckStrategy(BaseWolfliveStrategyInterface,GetMessageStrategyInterface):
    """responsible for checking states

    Args:
        BaseWolfliveStrategyInterface (_type_): _description_
        GetMessageStrategyInterface (_type_): _description_
    """
    def is_bot(self):
        print("\n\n is_bot()")
        """return true if last message is from a bot"""
        return self.get_last_element().get_attribute("is-bot")==''

    def is_stop(self):
        print("\n\n is_stop()")
        return bool(re.findall(r'!stop',self.get_last_user_msg() or '',re.I))


    def message_box_exists(self,private:Optional[bool]=False):
        self.goto_private() if private else self.goto_group()
        d = "user" if private else "group"
        return self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "app-routes",
            f"{d}-chat-page",
            "palringo-chat",
            "palringo-chat-input",
            "iron-autogrow-textarea",
        ).getOne("textarea").exists()

    def message_box_exists_group(self):
        return self.message_box_exists(private=False)

    def message_box_exists_private(self):
        return self.message_box_exists(private=True)


    def is_stop(self):
        print("\n\n is_stop()")
        return bool(re.findall(r'!stop',self.get_last_user_msg() or '',re.I))


class SendMessageStrategy(BaseWolfliveStrategyInterface,GetMessageStrategyInterface):
    """responsible for output actions

    Args:
        BaseWolfliveStrategyInterface (_type_): _description_
        GetMessageStrategyInterface (_type_): _description_
    """

    def send_msg(self, msg:str,private:bool=False):
        print(f"\n\n send_msg(private={private})")
        self.goto_private() if private else self.goto_group()
        d = "user" if private else "group"
        # Enter Msg

        self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "app-routes",
            f"{d}-chat-page",
            "palringo-chat",
            "palringo-chat-input",
            "iron-autogrow-textarea",
        ).getOne("textarea").execute().send_keys(msg.strip(),Keys.RETURN)
        


    def send_message_private(self, msg):
        self.send_msg(msg,private=True)

    def send_message_group(self, msg):
        self.send_msg(msg,private=False)

    def toggle_autoplay(self,cmd):
        print("\n\n toggle_autoplay()")
        self.send_msg(cmd)

    def check_autoplay(self,cmd,config_section):
        print("\n\n check_autoplay()")
        self.send_msg(cmd)
        for _ in range(20):
            if self.is_bot():
                break
            self.tracker.wait(seconds=0.3)
        text = self.get_last_bot_msg()
        if config[config_section.title()]['autoplay'].upper() not in text:
            self.toggle_autoplay(cmd)

    def change_inbox(self):
        print("\n\n change_inbox()")
        self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout"
        ).getOne("paper-drawer-panel").getOneShadowRoot(
            "palringo-sidebar",
            "paper-tabs"
        ).getOne("paper-tab[title='Chats']").action(".click()").execute()



class LoginStrategy(BaseWolfliveStrategyInterface,CheckStrategyInterface):
    username:str
    password:str
    private_url:Optional[str] ='https://wolf.live/u/80277459'
    room_link:Optional[str] = 'https://wolf.live/g/18900545'

    
    # def refresh_if_not_textbox(self,private=False):
    #     res = self.message_box_exists(private=private)
    #     if not res:
    #         self.driver.refresh()

    #     return res
        
    

    def set_driver(self):
        if getattr(self,"driver",None):
            self.driver.quit()
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_path)
        self.driver.set_page_load_timeout(80)
        self.is_login = False

    def update_driver(self):
        self.login()

    def login(self):
        print("\n\n login()")
        assert self.username and self.password,"username and password is required to login bot"
        self.set_driver()
        self.driver.implicitly_wait(10)
        
        

        try:
            for retry in range(7):
                try:
                    self.__login()
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

    def __login(self):
        print("\n\n login()")
        self.driver.get(self.room_link)
        self.tracker.wait(seconds=10)
        
        if self.qs.getOneShadowRoot(
            "palringo-install-android",
        ).getOne("#androidDismissButton").exists():
            try:
                self.qs.getOneShadowRoot("palringo-install-android").getOne(
                    "#androidDismissButton"
                ).execute().click()
            except:
                pass
            print("\n\n clicked androidDismissButton")

        self.tracker.wait(seconds=10)
        self.qs.getOneShadowRoot(
            "route-layout",
            "sidebar-layout",
            "palringo-sidebar",
            "palringo-sidebar-profile"
        ).getOne("#status").execute().click()
        self.qs.getOneShadowRoot("login-dialog").getOne("#palringo-login").execute().click()
        
        self.tracker.wait(seconds=6)
        
        self.qs.getOneShadowRoot("login-dialog")\
            .getOne("#email")\
        .execute().send_keys(self.username)
        self.tracker.wait(seconds=6)
        self.qs.getOneShadowRoot("login-dialog")\
            .getOne("#password")\
            .execute().send_keys(self.password)
        self.tracker.wait(seconds=8)
        self.qs.getOneShadowRoot("login-dialog")\
            .getOne("#sign-in").execute().click()
        self.tracker.wait(seconds=6)
        self.tracker.wait_til_condition(
            function=self.driver.refresh,
            conditions=[
                self.message_box_exists
            ],
            delay_in_seconds=4,
            max_loop=10
        )
        


@dataclass
class TestClass(BaseWolfliveStrategy,LoginStrategy,GetMessageStrategy,SendMessageStrategy,CheckStrategy):
    username:str
    password:str
    private_url:Optional[str] ='https://wolf.live/u/80277459'
    room_link:Optional[str] = 'https://wolf.live/g/18900545'
