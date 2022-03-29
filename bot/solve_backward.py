from dataclasses import dataclass,field
import re
import time
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy




@dataclass
class SolveBackward(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str = field(default_factory=lambda:'https://wolf.live/g/18477646')
    autoplay:bool = field(default_factory=lambda:False,init=False)
    game_start:bool = field(default_factory=lambda:False,init=False)
    stop:bool = field(default_factory=lambda:False,init=False)
    def __post_init__(self):
        self.login()
        self.setup_status()
        if self.autoplay:
            while True and not self.stop:
                try:
                    self.main()
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:

                    if self.stop:break
                    self.main()
                except Exception as e:
                    print("error from main method\n",e)

    def main(self):
        while True:
            try:
                if self.autoplay:
                    if not self.game_start:
                        self.send_msg('!backwards')
                        self.game_start = True
                else:
                    self.send_msg('!backwards')
                    self.game_start = True

                break
            except:
                continue
        while True:
            text = self.get_last_msg()
            if self.is_question(text=text):
                self.driver.implicitly_wait(20)
                answer =  self.get_answer(text=text)

                if answer:
                    self.send_msg(answer)

            if self.is_done(text):
                print("we have a winner\n",text)
                break

            if self.is_stop_game():
                print("you stoped the game")
                self.stop = True
                break

    

    def setup_status(self):
        if str(input("play game with auto mood (yes/no):\n===>")).lower() == 'yes':
            self.autoplay = True
        status:str = self.check_autoplay_status()
        print("status",status)
        if status.upper()=='ON':
            if not self.autoplay:
                self.toggle_autoplay()
        elif status.upper()=='OFF':
            if self.autoplay:
                self.toggle_autoplay()
        else:
            self.toggle_autoplay()
    
    def check_autoplay_status(self):
        self.send_msg('!backwards autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r"Autoplay is now turned (ON|OFF)",response,re.I)
        print("result from regex",res)
        if res:
            return res[0]
        else:
            raise Exception("site features has change update bot")
            # return False
        
    def wait_and_get_bot_message(self):
        end_time = time.time() + 40
        while time.time() < end_time:
            text = self.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text

    def wait_and_get_user_message(self):
        end_time = time.time() + 40
        while time.time() < end_time:
            text = self.get_last_msg()
            if not re.search('bot\n',text,re.IGNORECASE):
                return text

    def toggle_autoplay(self):
        self.send_msg('!backwards autoplay')

    def is_stop_game(self):
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except:
            self.driver.refresh()
            return

    def is_question(self,text):
        return bool(re.search(r"-->",text,flags=re.IGNORECASE))
            

    def get_answer(self,text=''):
        return re.findall(r'--> ([a-zA-Z0-9]+) <--',text)[0][::-1]


    def is_done(self,text=''):
        return bool(re.search(r'Congrats',text,flags=re.IGNORECASE))
        

    



    


if __name__ == '__main__':
    username_1 = 'theloveeyes@yandex.ru'
    password_1 = '951753'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18477646'
    
    s:SolveBackward = None
    
    for _ in range(5):
        try:
            s = SolveBackward(username_1, password_1,room_link)
            break
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    
    if s:s.tracker.wait(2)
    
    if s:s.close()