from dataclasses import dataclass
import re
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy

@dataclass
class WebDriver(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str
    private_url:str


class SolveTaboo:

    def __init__(self,browser:WebDriver,browser2:WebDriver):
        self.browser = browser
        self.browser2 = browser2
        self.browser.driver.switch_to.window(self.browser.driver.window_handles[0])
        for _ in range(int(input("how many time should i play the game?\n   e.g 100\n===> "))):
            try:
                self.main()
            except Exception as e:
                print("error occurred\n",e)


    def wait_for_bot_message_private(self):
        while True:
            if self.is_bot_message_private():
                return self.browser.get_last_message_private()

    def wait_for_bot_message_grp(self):
        while True:
            if self.is_bot_message_grp():
                return self.browser.get_last_msg()


    def is_bot_message_grp(self):
        return bool(re.search(r'bot',self.browser.get_last_msg(),re.I))

    def is_bot_message_private(self):
        return bool(re.search(r'bot',self.browser.get_last_message_private(),re.I))


    

    def is_timeup(self):
        return bool(re.search(r'Times up',self.browser.get_last_message_private(),re.I))
        





    def get_question_and_options(self,text=''):
        pass



    def main(self):
        while True:
            try:
                self.browser.send_msg("!taboo")
                break
            except:
                continue
        self.wait_for_bot_message_grp()
        self.browser.goto_private()
        text = self.browser.get_last_message_private()
        answer = re.findall(r'guess: ([a-zA-Z0-9 ]+\n?)',text,flags=re.I)[0]
        self.browser2.send_msg(answer)
        self.browser.goto_group()



        
if __name__ == '__main__':
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18512393'
    private_url = 'https://wolf.live/u/24957563'
    

    browser = None
    browser2 = None
    is_login = False
    
    
    for _ in range(5):
        try:
            browser = WebDriver(username_1, password_1,room_link,private_url)
            browser2 = WebDriver(username_2, password_2,room_link,private_url)
            browser.driver.execute_script(f"window.open('{private_url}');")
            is_login = True
            break
        except KeyboardInterrupt:
            break
        except:
            print("no internet conenction,re-trying...")
            continue
    
    browser.tracker.wait(2)
    if is_login:SolveTaboo(browser,browser2)
    if browser:browser.driver.quit()
    if browser2:browser2.driver.quit()