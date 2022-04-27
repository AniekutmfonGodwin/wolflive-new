from dataclasses import dataclass
import re
from main import *
from strategies.exceptions import StopBotError
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

    def __post_init__(self):
        self.login()


class SolveTaboo:

    def __init__(self,browser:WebDriver,browser2:WebDriver,test=False):
        self.browser = browser
        self.browser2 = browser2
        self.browser.driver.switch_to.window(self.browser.driver.window_handles[0])
        self.test = test
        self.browser.tracker.restart = self.restart
        self.browser.tracker.start()
        for _ in range(int(input("how many time should i play the game?\n   e.g 100\n===> ") or 100)):
            try:
                if not self.test:self.main()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print("error occurred\n",e)

    def restart(self):
        self.main()


    def wait_for_bot_message_private(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_for_bot_message_private()")
        while True:
            try:
                if self.is_bot_message_private():
                    return self.browser.get_last_message_private()
            except KeyboardInterrupt:
                raise KeyboardInterrupt



    def is_bot_message_grp(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_bot_message_grp()")
        return bool(re.search(r'bot',self.browser.get_last_msg(),re.I))

    def is_bot_message_private(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_bot_message_private()")
        return bool(re.search(r'bot',self.browser.get_last_message_private(),re.I))


    def is_timeup(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_timeup()")
        return bool(re.search(r'Times up',self.browser.get_last_message_private(),re.I))
        


    def get_question_and_options(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_question_and_options()")
        pass



    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        self.browser.tracker.start()
        while True:
            try:
                self.browser.send_msg("!taboo")
                self.browser.wait_for_bot_group()
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except StopBotError:
                raise StopBotError
            except Exception as e:
                print(f"\n\n error \n\n[{self.__class__}]{self.__class__.__name__}().main({e})")
                continue

        
        self.browser.goto_private()
        text = self.browser.get_last_message_private()
        answer = re.findall(r'guess: ([a-zA-Z0-9 ]+\n?)',text,flags=re.I)[0]
        self.browser2.send_msg(answer)
        self.browser2.wait_for_bot_group()
        self.browser.goto_group()
        self.browser.tracker.reset()




def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
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
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    browser.tracker.wait(2)
    if is_login:SolveTaboo(browser,browser2)
    if is_login:
        if browser:browser.driver.quit()
        if browser2:browser2.driver.quit()


def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
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
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    browser.tracker.wait(2)
    return SolveTaboo(browser,browser2,test=True)
    # if is_login:
    #     if browser:browser.driver.quit()
    #     if browser2:browser2.driver.quit()

if __name__ == '__main__':
    main()