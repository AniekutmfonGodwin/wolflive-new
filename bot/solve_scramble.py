from dataclasses import dataclass,field
import re
import json
import time
from main import *
from threading import Timer
from strategies.exceptions import StopBotError

from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy



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

    def __post_init__(self):
        self.login()
        # self = browser
        # self.words_file = words_file_dir
        # self.autoplay = False
        # self.game_start = False
        # self.timer = None
        # self.stop_game = False
        self.setup_status()
        if self.autoplay:
            while True and not self.stop_game:
                try:
                    self.main()
                except KeyboardInterrupt:
                    raise StopBotError
                except StopBotError:
                    raise StopBotError
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:
                    self.main()
                    if self.stop_game:break
                except KeyboardInterrupt:
                    raise StopBotError
                except StopBotError:
                    raise StopBotError
                except Exception as e:
                    print("error from main method\n",e)



    
    def setup_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().setup_status()")
        if str(input("play game with auto mood (yes/no):\n===>")).lower() == 'yes':
            self.autoplay = True
        status = self.check_autoplay_status()
        if status=='ON':
            if not self.autoplay:
                self.toggle_autoplay()
        elif status=='OFF':
            if self.autoplay:
                self.toggle_autoplay()
        # else:
        #     self.toggle_autoplay()


    
    def check_autoplay_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().check_autoplay_status()")
        self.send_msg('!scramble autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay .* (On|Off)',response,re.I)
        if res:
            return res[0]
        else:
            False
        
    
    def toggle_autoplay(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().toggle_autoplay()")
        self.send_msg('!scramble autoplay')
        self.wait_and_get_user_message()

    
    def wait_and_get_user_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_user_message()")
        for _ in range(40):
            text = self.get_last_element().text
            if not re.search('bot\n',text,re.IGNORECASE):
                return text
            self.tracker.wait(1)

    def wait_and_get_bot_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_bot_message()")
        for _ in range(40):
            text = self.get_last_element().text
            if re.search('bot\n',text,re.IGNORECASE):
                return text
            self.tracker.wait(1)

    def is_stop_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game()")
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except KeyboardInterrupt:
            raise StopBotError
        except StopBotError:
            raise StopBotError
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
                        if self.is_done(self.get_last_msg()):
                            break
                            print("answer is :",answer)

                    time.sleep(4)
                    if not self.is_done(self.get_last_msg()):
                        self.send_msg('!scramble next')
                else:
                    self.send_msg('!scramble next')

                

                
                    
            
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
                    else:
                        self.send_msg('!scramble next')
                else:
                    self.send_msg('!scramble')
                break
            except KeyboardInterrupt:
                raise StopBotError
            except StopBotError:
                raise StopBotError
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
    import os
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    file_path = os.path.join(os.path.dirname(__file__),"words_dictionary.json")
    
    room_link = 'https://wolf.live/g/18900545'
    

    browser:SolveScramble = None
    
    
    for _ in range(5):
        try:
            browser = SolveScramble(username_1, password_1,file_path,room_link)
            break
        except KeyboardInterrupt:
            raise StopBotError
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print("error",e)
            print("no internet conenction,re-trying...")
            continue
    
    
    if browser:browser.close()



if __name__ == '__main__':
    main()


    