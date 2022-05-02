from dataclasses import dataclass,field
import re
from typing import Any, Dict
from main import *
from strategies.exceptions import SignalRestartError, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from pathlib import Path
import configparser
import sys

config_file = os.path.join(Path(__file__).resolve().parent.parent,"config.ini")
config = configparser.ConfigParser()
config.read(config_file)

commands = {
    "is_question":r"لعبة فردية:",
    "get_answer":r'\{(.+)\} بعد مرور (\d+) ثانية',
    "is_gameover":r'انتهت اللعبة',
    "is_done":r'الفائز',
    "is_stop_game":r'قف!|!stop|!قف',
    "start_game":"!وقت"
}

commands_en = {
    "is_question":r"seconds from now to win",
    "get_answer":r'Type \{(.+)\} (\d+) seconds from now to win!',
    "is_gameover":r"Time's Up",
    "is_done":r'The winner',
    "is_stop_game":r'قف!|!stop|!قف',
    "start_game":"!timing"
}



@dataclass
class SolveTimming(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str
    stop:bool = field(default_factory=bool)
    commands:Dict[str,Any] = field(default_factory=lambda: commands_en)
    test:bool = field(default_factory=bool)
    autoplay:bool = field(default_factory=bool)
    bot_start_game:bool = field(default_factory=bool)
    

    def __post_init__(self):
        self.login()
        if not self.test:
            self.autoplay = config["Timing"]["autoplay"].lower().strip() in ["on","yes","1",1]
            self.bot_start_game = config["Timing"]["bot_start_game"].lower().strip() in ["yes","1",1]
            self.set_autoplay("!timing autoplay")
            if not self.test:self.restart()
    
    

    def restart(self):
        while True and not self.stop:
            try:
                self.main()
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except Exception as e:
                print("error occurred\n",e)

    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        if self.bot_start_game:self.start_game()
                
        while True:
            if self.is_question():
                answer =  self.get_answer()
                print("\n\n answer\nإجابة",answer)
                if answer:
                    self.tracker.wait(float(answer[1])-1.6)
                    if self.is_stop():
                        self.stop = True
                        print("\n\n stopped game")
                        break
                    self.send_msg(answer[0])


            if self.is_stop():
                self.stop = True
                print("stopped game")
                break

            if self.is_gameover():
                print("game over\nانتهت اللعبة")
                self.start_game()

            if self.is_done():
                print("we have a winner\nلدينا فائز")
                if not self.autoplay:
                    self.start_game()


    def wait_and_get_bot_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_bot_message()")
        while True:
            text = self.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text

    def is_question(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        return bool(re.search(self.commands.get("is_question"),self.get_last_msg(),flags=re.IGNORECASE))

    def get_answer(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        return re.findall(self.commands.get("get_answer"),self.get_last_msg())[0]
        

    

    def is_gameover(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_gameover()")
        return bool(re.search(self.commands.get("is_gameover"),self.get_last_msg(),flags=re.IGNORECASE))
        

    def is_done(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        return bool(re.search(self.commands.get("is_done"),self.get_last_msg(),flags=re.IGNORECASE))
        

    def is_stop_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game()")
        try:
            return bool(re.findall(self.commands.get("is_stop_game"),self.get_last_msg(),flags=re.IGNORECASE))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            self.close()
            raise SignalRestartError
        except Exception as e:
            self.driver.refresh()
            print(f"\n\n error\n\n[{self.__class__}]{self.__class__.__name__}().is_stop_game({e})")
            return

    def start_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game()")
        for _ in range(10):
            try:
                # self.browser.send_msg('!timing')
                self.send_msg(self.commands.get("start_game"))
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except StopBotError:
                raise StopBotError
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except Exception as e:
                print(f"\n\n error \n\n[{self.__class__}]{self.__class__.__name__}().start_game({e})")
                continue
        


def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    
    browser = None
    
    for _ in range(5):
        try:
            browser:SolveTimming = SolveTimming(username_1, password_1,room_link)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            continue
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    if browser:browser.driver.quit()


def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    
    browser = None
    
    for _ in range(5):
        try:
            browser = SolveTimming(username_1, password_1,room_link,test=True)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            continue
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            if browser and browser.driver:browser.driver.quit()
            continue
    return browser
    # if browser:browser.driver.quit()
    
    
    

if __name__ == '__main__' and "-i" not in sys.argv:
    main()


    


    # def answer_lyrics(self,question):