from dataclasses import dataclass
from datetime import timedelta
import os
import re
from typing import List, Optional
from query_builder import QueryBuilder
from selenium import webdriver
from strategies.exceptions import StopBot, StopBotError
from strategies.interfaces import BaseWolfliveStrategyInterface, CheckStrategyInterface, GetMessageStrategyInterface, LoginStrategyInterface, SendMessageStrategyInterface
from utils.helpers import Tracker
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import configparser
from selenium.common.exceptions import JavascriptException

config_file = os.path.join(Path(__file__).resolve().parent.parent,"config.ini")
config = configparser.ConfigParser()
config.read(config_file)



url = 'https://wolf.live/'
chrome_options = Options()
chrome_options.add_experimental_option('w3c', True)
absolute_path = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(absolute_path, '../chromedriver')







class BaseWolfliveStrategy(CheckStrategyInterface):
    selectors:List[str]=list()
    driver:webdriver.Chrome
    

    def goto_group(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().goto_group()")
        self.driver.switch_to.window(self.driver.window_handles[0])
        

    def goto_private(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().goto_private()")
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
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().close()")
        self.driver.quit()




class GetMessageStrategy(BaseWolfliveStrategyInterface,CheckStrategyInterface):
    """responsible for getting input

    Args:
        BaseWolfliveStrategyInterface (_type_): _description_
    """
    def get_last_msg(self,index=-1):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_msg(index={index})")
        """
        function get the latestest message in test form
        """
        try:
            elements = self.get_latest_msgs().execute()
            element = elements[index]
            return self.qs.action(".shadowRoot").getOne("palringo-chat-message-text").execute(element).text
        except:
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() could not retrieve last element")
            return ''

    def get_latest_msgs(self,private=False):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_latest_msgs(private={private})")
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
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_latest_user_msgs()")
        elements = self.get_latest_msgs().execute()
        return [x for x in elements if x.get_attribute("is-bot")!='']

    def get_latest_bot_msgs(self,private=False)-> List[WebElement]:
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_latest_bot_msgs(private={private})")
        return [x for x in self.get_latest_msgs(private=private).execute() if x.get_attribute("is-bot")=='']

    def get_last_message_private(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_message_private()")
        self.goto_private()
        self.driver.implicitly_wait(20)
        elements = self.get_lastest_messages_private().execute()
        if not elements:
            return ''
        return elements[-1].text

    def get_lastest_messages_private(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_lastest_messages_private()")
        self.goto_private()
        return self.get_latest_msgs(private=True)

    def get_latest_msgs(self, private: bool = False):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_latest_msgs(private = {private})")
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
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_bot_msg({index},{private})")
        """
        function get the latestest message in test form
        """
        self.goto_private() if private else self.goto_group()
        try:
            return self.qs.action(".shadowRoot").getOne('palringo-chat-message-text').execute(self.get_latest_bot_msgs(private=private)[index]).text
        except:
            return ''




    def get_last_user_msg(self,index=-1):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_user_msg({index})")
        """
        function get the latestest message in test form
        """
        try:
            elements = self.get_latest_user_msgs()
            if not elements:
                return ""
            element = elements[index]
            return self.qs.action(".shadowRoot")\
                .getOne("palringo-chat-message-text")\
                    .execute(element).text
        except Exception as e:
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() error while getting user message ",e)
            return ''
        




    def get_latest_pm(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_latest_pm()")
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
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_element({index})")
        """
        function get the latestest message in test form
        """
        elements = self.get_latest_msgs().execute()
        assert elements," could not find last element when get_last_element() was called "
        return elements[index]

        




class CheckStrategy(BaseWolfliveStrategyInterface,LoginStrategyInterface,GetMessageStrategyInterface):
    """responsible for checking states

    Args:
        BaseWolfliveStrategyInterface (_type_): _description_
        GetMessageStrategyInterface (_type_): _description_
    """
    def is_bot(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_bot()")
        """return true if last message is from a bot"""
        return self.get_last_element().get_attribute("is-bot")==''

    def is_stop(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop()")
        return bool(re.findall(r'!stop',self.get_last_user_msg() or '',re.I))

    @property
    def is_login(self):
        try:
            res = bool(self.qs.getOneShadowRoot("route-layout","sidebar-layout","palringo-sidebar","palringo-sidebar-profile","palringo-user-avatar").getOne("#avatar").execute().get_attribute("src"))
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_login({res})")
            return res
        except StopBotError:
            raise StopBotError()
        except Exception as e:
            print(e)
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_login(False)")
            return False
        
            


    def message_box_exists(self,private:Optional[bool]=False):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().message_box_exists({private})")
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
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().message_box_exists_group()")
        return self.message_box_exists(private=False)

    def message_box_exists_private(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().message_box_exists_group()")
        return self.message_box_exists(private=True)


    def is_stop(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop()")
        return bool(re.findall(r'!stop',self.get_last_user_msg() or '',re.I))

    @property
    def is_debug(self):
        return (config["settings"]["DEBUG"] or '').strip().lower() in ["true",1,'1']
        


class SendMessageStrategy(BaseWolfliveStrategyInterface,GetMessageStrategyInterface,CheckStrategyInterface):
    """responsible for output actions

    Args:
        BaseWolfliveStrategyInterface (_type_): _description_
        GetMessageStrategyInterface (_type_): _description_
    """

    def send_msg(self, msg:str,private:bool=False):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().send_msg(private={private})")
        for _ in range(20):
            try:
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
                break
            except JavascriptException:
                self.driver.refresh()
                self.tracker.wait(5)
    
    def wait_for_bot_group(self,*,count=500,delay_in_second=0.5):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_for_bot(count={count},delay_in_second={delay_in_second})")
        for _ in range(count):
            if "bot" in self.get_last_element().text.lower():break
            self.tracker.wait(delay_in_second)
        return self.get_last_element().text

    def wait_for_message_group(self,text,count=500,delay_in_second=0.5):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_for_bot(count={count},delay_in_second={delay_in_second})")
        for _ in range(count):
            if text in self.get_last_msg():break
            self.tracker.wait(delay_in_second)

        return self.get_last_msg()
            



    def send_message_private(self, msg):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().send_message_private({msg})")
        self.send_msg(msg,private=True)

    def send_message_group(self, msg):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().send_message_group({msg})")
        self.send_msg(msg,private=False)

    def toggle_autoplay(self,cmd):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().toggle_autoplay({cmd})")
        self.send_msg(cmd)
        self.wait_for_bot_group()
        

    def check_autoplay(self,cmd,config_section:str):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().check_autoplay({cmd},{config_section})")
        self.send_msg(cmd)
        self.wait_for_message_group(cmd)
        self.wait_for_bot_group()
        text = self.get_last_bot_msg()
        if config_section and config[config_section.title()]['autoplay'].upper() not in text:
            self.toggle_autoplay(cmd)

    def change_inbox(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().change_inbox()")
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

        

    def set_driver(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().set_driver()")
        if getattr(self,"driver",None):
            self.driver.quit()
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_path)
        self.driver.set_page_load_timeout(80)
        

    def update_driver(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().update_driver()")
        self.login()

    def login(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().login()")
        try:
            self.driver.quit()
        except Exception as e:
            pass

        assert self.username and self.password,"username and password is required to login bot"
        self.set_driver()
        self.driver.implicitly_wait(10)
        
        

        try:
            for retry in range(10):
                try:
                    self.__login()
                    self.tracker.wait(5)
                    if self.is_login:break
                except ConnectionRefusedError:
                    print("check you internet connection")
                    if retry > 5:
                        raise Exception("maximum retry has been reached")
                except TimeoutException:
                    if retry > 5:
                        raise Exception("maximum retry has been reached")
                self.tracker.wait(10)
                self.driver.refresh()
        except Exception as e:
            print(f"\n\n error \n\n[{self.__class__}]{self.__class__.__name__}().login({e})")
            self.driver.quit()
            raise StopBotError(f"couldn't login {e}")

    def __login(self):
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().login()")
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
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() clicked androidDismissButton")

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
        self.tracker.wait(seconds=5)
        # self.driver.refresh()
        # self.tracker.wait(seconds=5)
        # if self.is_login:
        #     self.tracker.wait_til_condition(
        #         function=self.driver.refresh,
        #         conditions=[
        #             self.message_box_exists
        #         ],
        #         delay_in_seconds=4,
        #         max_loop=10
        #     )

@dataclass
class TestClass(BaseWolfliveStrategy,LoginStrategy,GetMessageStrategy,SendMessageStrategy,CheckStrategy):
    username:str
    password:str
    private_url:Optional[str] ='https://wolf.live/u/80277459'
    room_link:Optional[str] = 'https://wolf.live/g/18900545'

    def restart(self):
        print("restart called")

def main():
    password = "123456"
    username = "Komp@gmail.com"
    return TestClass(username,password)
    
    # return t.tracker


if __name__ == '__main__':
    main()
    
