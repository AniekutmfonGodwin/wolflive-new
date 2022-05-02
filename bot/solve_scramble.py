from dataclasses import dataclass,field
import re
import json
import time
from main import *
from threading import Timer
from strategies.exceptions import SignalRestartError, StopBotError
import os
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from pathlib import Path
import configparser
import sys

config_file = os.path.join(Path(__file__).resolve().parent.parent,"config.ini")
config = configparser.ConfigParser()
config.read(config_file)

file_path = os.path.join(Path(__file__).resolve().parent,"words_dictionary.json")



@dataclass
class SolveScramble(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    words_file:str
    room_link:str
    autoplay:bool = field(default_factory=bool)
    game_start:bool = field(default_factory=bool)
    timer:bool = field(default_factory=lambda:None)
    stop_game:bool = field(default_factory=lambda:None)
    loop_count:int = field(default_factory=int)
    test:bool = field(default_factory=bool)

    def __post_init__(self):
        self.login()
        self.autoplay = config["Scramble"]["autoplay"].lower() in ["on",1,"1"]
        self.set_autoplay('!scramble autoplay')
        if not self.test:self.restart()
        

    def restart(self):
        if self.autoplay:
            while True and not self.stop_game:
                try:
                    self.main()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except StopBotError:
                    raise StopBotError
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            self.loop_count = self.loop_count or int(input("how many times do you want to play the game?\ne.g 200\n===>") or 200)
            for _ in range(self.loop_count):
                self.loop_count -= 1
                try:
                    self.main()
                    if self.stop_game:break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except StopBotError:
                    raise StopBotError
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except Exception as e:
                    print("error from main method\n",e)
            raise StopBotError

    
    

    def is_stop_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game()")
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            self.close()
            raise SignalRestartError
        except Exception as e:
            print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game({e})")
            self.driver.refresh()
            return

    
    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        self.start_game()
        while True:
            
            text = self.get_last_msg()
            if self.is_question(text=text):
                answers =  self.get_answer(self.get_question(text))
                if answers:
                    for answer in answers:
                        self.send_msg(answer)
                        self.wait_for_bot_group()
                        if self.is_done(self.get_last_msg()):
                            print("answer is :",answer)
                            break

                    time.sleep(4)
                    if not self.is_done(self.get_last_msg()):
                        self.send_msg('!scramble next')
                        self.wait_for_bot_group()
                else:
                    self.send_msg('!scramble next')
                    self.wait_for_bot_group()

                

                
                    
            
            if self.is_done(text):
                
                print("\n\n we have a winner\n",text)
                self.game_start=False
                break

            if self.is_bot(text):
                check_timer = self.timer
                if check_timer:check_timer.cancel()
                t=Timer(15.0,self.start_game)
                self.timer=t
                t.start()

            if self.is_stop_game():
                self.stop_game = True
                break
                

    

    def is_question(self,text):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        return bool(re.search(r"\|>",text,flags=re.IGNORECASE))
            

    def get_answer(self,question=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        with open(self.words_file) as words:
            words = (x for x in list(json.load(words)))
        return [word for word in words if sorted(question) == sorted(word) and word[0] == question[0] and word[-1] == question[-1]]


    def start_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game()")
        for _ in range(10):
            try:
                if self.autoplay:
                    if not self.game_start:
                        self.send_msg('!scramble')
                        self.wait_for_bot_group()
                    else:
                        self.send_msg('!scramble next')
                        self.wait_for_bot_group()
                else:
                    self.send_msg('!scramble')
                    self.wait_for_bot_group()
                break
            except KeyboardInterrupt:
                raise StopBotError
            except StopBotError:
                raise StopBotError
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except Exception as e:
                print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().start_game({e})")
                continue
        self.game_start=True
        
            
    

    def is_done(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        return bool(re.search(r'Congrats',text,flags=re.IGNORECASE))

    def is_bot(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_bot()")
        return bool(re.search(r'bot',text,flags=re.IGNORECASE))
        

    def get_question(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_question()")
        return re.findall(r'\|> ([a-zA-Z0-9]+) <\|',text)[0]



def main():
    
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    
    
    room_link = 'https://wolf.live/g/18900545'
    

    browser:SolveScramble = None
    
    
    for _ in range(5):
        try:
            browser = SolveScramble(username_1, password_1,file_path,room_link,loop_count=getattr(SolveScramble,"loop_count",0))
            browser.close()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveScramble.loop_count = browser.loop_count
            continue
        except Exception as e:
            print("error",e)
            print("no internet conenction,re-trying...")
            continue
    
    
    


def test():
    
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    
    
    room_link = 'https://wolf.live/g/18900545'
    

    browser:SolveScramble = None
    
    
    for _ in range(5):
        try:
            return SolveScramble(username_1, password_1,file_path,room_link,loop_count=getattr(SolveScramble,"loop_count",0),test=True)
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveScramble.loop_count = browser.loop_count
            browser.close()
            continue
        except Exception as e:
            print("error",e)
            print("no internet conenction,re-trying...")
            continue
    
    
    if browser:browser.close()



if __name__ == '__main__' and "-i" not in sys.argv:
    main()


    