from dataclasses import dataclass
import re
from main import *
from strategies.exceptions import SignalRestartError, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
import sys


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
    loop_count:int = 0
    def __init__(self,browser:WebDriver,browser2:WebDriver,test=False,loop_count=int):
        self.browser = browser
        self.browser2 = browser2
        self.browser.driver.switch_to.window(self.browser.driver.window_handles[0])
        self.test = test
        self.loop_count = loop_count
        if not self.test:self.restart()
    
    def close(self):
        try:
            self.browser.close()
            self.browser2.close()
        except:
            pass

    def restart(self):
        self.loop_count = self.loop_count or int(input("how many time should i play the game?\n   e.g 100\n===> ") or 100)
        for _ in range(self.loop_count):
            self.loop_count -=1
            try:
                if not self.test:self.main()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except StopBotError:
                raise StopBotError
            except Exception as e:
                print("error occurred\n",e)

        raise StopBotError


    def wait_for_bot_message_private(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_for_bot_message_private()")
        while True:
            if self.is_bot_message_private():
                return self.browser.get_last_message_private()
            



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
        while True:
            try:
                self.browser.send_msg("!taboo")
                self.browser.wait_for_bot_group()
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except StopBotError:
                raise StopBotError
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except Exception as e:
                print(f"\n\n error \n\n[{self.__class__}]{self.__class__.__name__}().main({e})")
                continue

        
        self.browser.goto_private()
        text = self.browser.get_last_message_private()
        answer = re.findall(r'guess: ([a-zA-Z0-9 ]+\n?)',text,flags=re.I)[0]
        self.browser2.send_msg(answer)
        self.browser2.wait_for_bot_group()
        self.browser.goto_group()




def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    private_url = 'https://wolf.live/u/24957563'
    
    browser = None
    browser2 = None
    taboo:SolveTaboo = None
    
    
    for _ in range(20):
        try:
            browser = WebDriver(username_1, password_1,room_link,private_url)
            browser2 = WebDriver(username_2, password_2,room_link,private_url)
            browser.driver.execute_script(f"window.open('{private_url}');")
            browser.tracker.wait(2)
            taboo = SolveTaboo(browser,browser2,loop_count=getattr(SolveTaboo,"loo_count",0))
            if browser:browser.driver.quit()
            if browser2:browser2.driver.quit()
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveTaboo.loop_count = taboo.loop_count
            continue
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    


def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    private_url = 'https://wolf.live/u/24957563'
    
    browser = None
    browser2 = None
    taboo:SolveTaboo = None
    
    
    for _ in range(20):
        try:
            browser = WebDriver(username_1, password_1,room_link,private_url)
            browser2 = WebDriver(username_2, password_2,room_link,private_url)
            browser.driver.execute_script(f"window.open('{private_url}');")
            browser.tracker.wait(2)
            return SolveTaboo(browser,browser2,loop_count=getattr(SolveTaboo,"loop_count",0))
            
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveTaboo.loop_count = taboo.loop_count
            taboo.close()
            continue
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue

if __name__ == '__main__' and "-i" not in sys.argv:
    main()