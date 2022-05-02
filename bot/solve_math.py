from dataclasses import dataclass,field
import re
from main import *
from strategies.exceptions import SignalRestartError, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from pathlib import Path
import configparser
import sys

config_file = os.path.join(Path(__file__).resolve().parent.parent,"config.ini")
config = configparser.ConfigParser()
config.read(config_file)


@dataclass
class SolveMathsBot(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str
    autoplay:bool = field(default_factory=bool,init=False)
    game_start:bool = field(default_factory=bool,init=False)
    stop:bool = field(default_factory=bool,init=False)
    loop_count:int = field(default_factory=int)
    test:bool = field(default_factory=bool)

    def __post_init__(self):
        self.login()
        self.autoplay = config["Math"]["autoplay"].lower().strip() in ["on","yes","1",1]
        self.set_autoplay("!math autoplay")
        if not self.test:self.restart()
        
                    
    def restart(self):
        if not self.is_login:self.update_driver()
        if self.autoplay:
            while True and not self.stop:
                try:
                    self.main()
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except StopBotError:
                    raise StopBotError
                except Exception as e:
                    print("error from main method\n")
                    continue
        else:
            self.loop_count = self.loop_count or int(input("how many times do you want to play the game?\ne.g 200\n===>") or 200)
            for _ in range(self.loop_count):
                self.loop_count -=1
                try:
                    if self.stop:break
                    self.main()
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except StopBotError:
                    raise StopBotError
                except:
                    continue
            raise StopBotError

    def start_game(self):
        for _ in range(10):
            if not self.game_start:
                try:
                    self.send_msg('!math')
                    self.wait_for_message_group("!math")
                    self.game_start = True
                    break
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except StopBotError:
                    raise StopBotError
                except:
                    self.tracker.wait(1)
                    continue

    def is_gameover(self):
        try:
            return bool(re.search(r'game over',self.get_last_msg(),flags=re.IGNORECASE))
        except:
            self.driver.refresh()
            return

            


    def main(self):
        self.start_game()
        while True:
            text = self.wait_for_bot_group()
            if self.is_question(text):
                answer =  self.get_answer(text=text)

                if answer:
                    self.send_msg(answer)
                    self.wait_for_message_group(answer)

            if self.is_done(text):
                # print("we have a winner\n",text)
                break
            if self.is_stop_game():
                self.stop = True
                break

            if self.is_gameover():
                self.game_start = False
                break



 

    def is_question(self,text=''):
        return bool(re.findall(r"The timer has begun",str(text),flags=re.IGNORECASE))

    def get_answer(self,text=''):
        res = re.findall(r'Solve: (.+)',text)
        if res:
            equation = re.sub(r'×','*',res[0])
            return str(int(eval(equation)))

    def is_done(self,text=''):
        return bool(re.findall(r'You got it',str(text),flags=re.IGNORECASE))

    def is_stop_game(self):
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except:
            self.driver.refresh()
            return



def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    # username_2 = 'Telek@gmail.com'
    # password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    

    browser:SolveMathsBot = None
    
    for _ in range(20):
        try:
            browser = SolveMathsBot(username_1, password_1,room_link,loop_count=getattr(SolveMathsBot,"loop_count",0))
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveMathsBot.loop_count = browser.loop_count
            continue
        # except Exception as e:
        #     print("no internet conenction,re-trying...",e)
        #     continue
    
    
    if browser:browser.close()


def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    # username_2 = 'Telek@gmail.com'
    # password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    

    browser:SolveMathsBot = None
    
    for _ in range(20):
        try:
            return SolveMathsBot(username_1, password_1,room_link,test=True,loop_count=getattr(SolveMathsBot,"loop_count",0))
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveMathsBot.loop_count = browser.loop_count
            continue
        # except Exception as e:
        #     print("no internet conenction,re-trying...",e)
        #     continue
    
    
    if browser:browser.close()


if __name__ == '__main__' and "-i" not in sys.argv:
    main()
    
    