# %%
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
from time import sleep
import sys
import time
import re
from random import randint
from utilities import get_proxy



username_1 = 'Komp@gmail.com'
password_1 = '123456'
username_2 = 'Telek@gmail.com'
password_2 = '123456'

# room_link = 'https://wolf.live/my+gams'
max_unscramble_tries = 4


url = 'https://wolf.live/'
chrome_options = Options()
absolute_path = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(absolute_path, '../../chromedriver')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.82 Mobile Safari/537.36")
# chrome_options.add_argument("--start-maximized")  # To open chrome in full screen
# with open('words.txt', 'r') as f:
#     dictionary = f.read()

# dictionary = [x.lower() for x in dictionary.split('\n')]

already_done_typed_msgs = []
already_done_scramble_msgs = []
already_done_timing_msgs = []








class WebDriver:
    def __init__(self, username, password,room_link):
        self.username = username
        self.password = password
        self.room_link = room_link
        # data = get_proxy()
        # assert data,"couldn't get proxy"
        # PROXY = data.replace('\n','')
        # print("proxy",PROXY)
        # webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #     "httpProxy":PROXY,
        #     "ftpProxy":PROXY,
        #     "sslProxy":PROXY,
        #     "proxyType":"MANUAL"
        # }
        # self.driver = webdriver.Chrome( executable_path=chromedriver_path)
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_path)
        self.driver.implicitly_wait(20)
        self.driver.set_page_load_timeout(80)
        sleep(2)
        try:
            self.login()
        except Exception as e:
            self.driver.quit()
            raise Exception("couldn't login",e)

    def expand_shadow_element(self, element):
        shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root


    def expand_all(self,data:list):
        


        sleep(2)
        
        result = self.driver.find_element_by_css_selector(data[0])
        for x in data[1:]:
            
            result = self.expand_shadow_element(result)
            result = result.find_element_by_css_selector(x)
            

        return result

    def login(self):
        self.driver.get(self.room_link)
        

        self.expand_all([
            "palringo-install-android",
            "#androidDismissButton"
        ]).click()



        self.expand_all([
            "route-layout",
            "sidebar-layout",
            "app-routes",
            "group-chat-page",
            "palringo-chat-pre-join",
            "#join"
        ]).click()

        


        
        self.driver.find_element_by_tag_name('route-layout')
        

        self.expand_all([
            "login-dialog",
            "#palringo-login"
        ]).click()
        
        
        
        self.expand_all([
            "login-dialog",
            "#email",
            "input"
        ]).send_keys(self.username)



        self.expand_all([
            "login-dialog",
            "#password",
            "input"
        ]).send_keys(self.password)


        self.expand_all([
            "login-dialog",
            "#sign-in"
        ]).click()


        # cancel already in the group modal
        self.expand_all([
            "group-join-dialog",
            ".cancel-button"
        ]).click()

      




    def send_msg(self, msg):
        

        # Enter Msg
        self.expand_shadow_element(
            self.expand_shadow_element(self.expand_shadow_element(self.expand_shadow_element(
                self.expand_shadow_element(self.expand_shadow_element(self.expand_shadow_element(
                    self.driver.find_element_by_tag_name('route-layout')).find_element_by_tag_name(
                    'sidebar-layout')).find_element_by_tag_name('paper-drawer-panel').find_element_by_tag_name(
                    'app-routes')).find_element_by_tag_name('group-chat-page')).find_element_by_tag_name(
                'palringo-chat')).find_element_by_tag_name('palringo-chat-input')).find_element_by_tag_name(
                'iron-autogrow-textarea')).find_element_by_tag_name('textarea').send_keys(msg.strip())

        self.expand_shadow_element(self.expand_shadow_element(self.expand_shadow_element(
            self.expand_shadow_element(self.expand_shadow_element(self.expand_shadow_element(
                self.driver.find_element_by_tag_name('route-layout')).find_element_by_tag_name(
                'sidebar-layout')).find_element_by_tag_name('paper-drawer-panel').find_element_by_tag_name(
                'app-routes')).find_element_by_tag_name('group-chat-page')).find_element_by_tag_name(
            'palringo-chat')).find_element_by_tag_name('palringo-chat-input')).find_element_by_id(
            'send-button').click()

    def get_latest_msgs(self):
        
        return self.expand_shadow_element(self.expand_shadow_element(
            self.expand_shadow_element(self.expand_shadow_element(self.expand_shadow_element(
                self.driver.find_element_by_tag_name('route-layout')).find_element_by_tag_name(
                'sidebar-layout')).find_element_by_tag_name('paper-drawer-panel').find_element_by_tag_name(
                'app-routes')).find_element_by_tag_name('group-chat-page')).find_element_by_tag_name(
            'palringo-chat')).find_element_by_id('chat-container').find_elements_by_tag_name('palringo-chat-message')

    def get_last_msg(self):
        """
        function get the latestest message in test form
        """
        return self.get_latest_msgs()[-1].text




    def get_latest_pm(self):
        self.driver.implicitly_wait (20)
        return self.expand_shadow_element (self.expand_shadow_element (
            self.expand_shadow_element (self.expand_shadow_element (self.expand_shadow_element (
                self.driver.find_element_by_tag_name ('route-layout')).find_element_by_tag_name (
                'sidebar-layout')).find_element_by_tag_name ('paper-drawer-panel').find_element_by_tag_name (
                'app-routes')).find_element_by_tag_name ('user-chat-page')).find_element_by_tag_name (
            'palringo-chat')).find_element_by_id ('chat-container').find_elements_by_tag_name ('palringo-chat-message')

    def change_inbox(self):
        self.expand_shadow_element (self.expand_shadow_element (self.expand_shadow_element (self.expand_shadow_element (
            self.driver.find_element_by_tag_name ('route-layout')).find_element_by_tag_name (
            'sidebar-layout')).find_element_by_tag_name ('paper-drawer-panel').find_element_by_tag_name (
            'palringo-sidebar')).find_element_by_tag_name ('paper-tabs')).find_element_by_xpath('//paper-tab[@title="Chats"]').click ()


# %%
# if __name__ == '__main__':
#     username_1 = 'Komp@gmail.com'
#     password_1 = '123456'
#     room_link = 'https://wolf.live/g/18405282'

#     browser = WebDriver(username_1, password_1,room_link)

#     # element = browser.expand_all(['route-layout','sidebar-layout','paper-drawer-panel','palringo-sidebar','palringo-sidebar-profile',"div","#status"])
    
#     browser.driver.get(browser.room_link)


#     browser.expand_all([
#         "palringo-install-android",
#         "#androidDismissButton"
#     ]).click()



#     browser.expand_all([
#         "route-layout",
#         "sidebar-layout",
#         "app-routes",
#         "group-chat-page",
#         "palringo-chat-pre-join",
#         "#join"
#     ]).click()

    


#     # browser.driver.implicitly_wait(20)
#     browser.driver.find_element_by_tag_name('route-layout')
#     # sleep(6)

#     browser.expand_all([
#         "login-dialog",
#         "#palringo-login"
#     ]).click()
    


    

    
#     # sleep(2)
#     browser.expand_all([
#         "login-dialog",
#         "#email",
#         "input"
#     ]).send_keys(browser.username)



#     browser.expand_all([
#         "login-dialog",
#         "#password",
#         "input"
#     ]).send_keys(browser.password)


#     browser.expand_all([
#         "login-dialog",
#         "#sign-in"
#     ]).click()
    
    # browser.driver.quit()

def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'

    room_link = 'https://wolf.live/g/18336134'

    browser = None
    is_login = False
    browser = WebDriver(username_1, password_1,room_link)

# %%

if __name__ == '__main__':
    main()
    
    