from dataclasses import dataclass,field
import re
import json
import time
from time import sleep
# from main import *
from threading import Timer

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
    room_link:str
    words_file:str
    autoplay:bool = field(default_factory=bool)
    game_start:bool = field(default_factory=bool)
    timer:bool = field(default_factory=lambda:None)
    stop_game:bool = field(default_factory=lambda:None)

    def __post_init__(self):
        self.login()
        # self.browser = browser
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
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:
                    self.main()
                    if self.stop_game:break
                except Exception as e:
                    print("error from main method\n",e)



    
    def setup_status(self):
        if str(input("play game with auto mood (yes/no):\n===>")).lower() == 'yes':
            self.autoplay = True
        status = self.check_autoplay_status()
        if status=='ON':
            if not self.autoplay:
                self.toggle_autoplay()
        elif status=='OFF':
            if self.autoplay:
                self.toggle_autoplay()
        else:
            self.toggle_autoplay()


    
    def check_autoplay_status(self):
        self.browser.send_msg('!scramble autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay is turned (ON|OFF)',response,re.I)
        if res:
            return res[0]
        else:
            False
        
    
    def toggle_autoplay(self):
        self.browser.send_msg('!scramble autoplay')
        self.wait_and_get_user_message()

    
    def wait_and_get_user_message(self):
        for _ in range(40):
            text = self.browser.get_last_msg()
            if not re.search('bot\n',text,re.IGNORECASE):
                return text
            sleep(1)

    def wait_and_get_bot_message(self):
        for _ in range(40):
            text = self.browser.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text
            sleep(1)

    def is_stop_game(self):
        try:
            return bool(re.findall(r'!stop',self.browser.get_last_msg(),flags=re.IGNORECASE))
        except:
            self.browser.driver.refresh()
            return

    
    def main(self):
        self.start_game()
        while True:
            
            text = self.browser.get_last_msg()
            if self.is_question(text=text):
                
                
                answers =  self.get_answer(self.get_question(text))
                if answers:
                    for answer in answers:
                        self.browser.send_msg(answer)
                        if self.is_done(self.browser.get_last_msg()):
                            break
                            print("answer is :",answer)

                    time.sleep(4)
                    if not self.is_done(self.browser.get_last_msg()):
                        self.browser.send_msg('!scramble next')
                else:
                    self.browser.send_msg('!scramble next')

                

                
                    
            
            if self.is_done(text):
                
                print("we have a winner\n",text)
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
        return bool(re.search(r"\|>",text,flags=re.IGNORECASE))
            

    def get_answer(self,question=''):
        with open(self.words_file) as words:
            words = (x for x in list(json.load(words)))
        return [word for word in words if sorted(question) == sorted(word) and word[0] == question[0] and word[-1] == question[-1]]


    def start_game(self):
        print("start game")
        for _ in range(10):
            try:
                if self.autoplay:
                    if not self.game_start:
                        self.browser.send_msg('!scramble')
                    else:
                        self.browser.send_msg('!scramble next')
                else:
                    self.browser.send_msg('!scramble')
                break
            except:
                continue
        self.game_start=True
        
            


    def is_done(self,text=''):
        return bool(re.search(r'Congrats',text,flags=re.IGNORECASE))

    def is_bot(self,text=''):
        return bool(re.search(r'bot',text,flags=re.IGNORECASE))
        

    def get_question(self,text=''):
        return re.findall(r'\|> ([a-zA-Z0-9]+) <\|',text)[0]
        


if __name__ == '__main__':
    import os
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    file_path = os.path.join(os.path.dirname(__file__),"words_dictionary.json")
    
    room_link = 'https://wolf.live/g/18336134'
    

    browser:SolveScramble = None
    
    
    for _ in range(5):
        try:
            browser = SolveScramble(username_1, password_1,room_link,file_path)
            break
        except Exception as e:
            print("error",e)
            print("no internet conenction,re-trying...")
            continue
    
    
    
    
    if browser:browser.close()


    