from dataclasses import dataclass,field
import re
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy



@dataclass
class SolveTyping(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str
    autoplay:bool = field(default_factory=bool)
    game_start:bool = field(default_factory=bool)

    def __post_init__(self):
        self.login()
        self.setup_status()
        if self.autoplay:
            while True:
                try:
                    self.main()
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:
                    self.main()
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
        self.send_msg('!typing autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay is turned (ON|OFF)',response,re.I)
        if res:
            return res[0]
        else:
            False
        

    def toggle_autoplay(self):
        self.send_msg('!typing autoplay')
        self.wait_and_get_user_message()


    def main(self):
        for _ in range(40):
            try:
                if self.autoplay:
                    if not self.game_start:
                        self.send_msg('!typing')
                else:
                    self.send_msg('!typing')
                break
            except:
                self.tracker.wait(1)
                continue

        self.game_start =True
        for _ in range(50):
            text = self.wait_and_get_bot_message()
            if self.is_question(text):
                answer =  self.get_answer(text=text)

                if answer:
                    self.send_msg(answer)
                    print("answer is :",answer)

            if self.is_done(text):
                print("we have a winner\n",text)
                break

    def wait_and_get_bot_message(self):
        for _ in range(40):
            text = self.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text
            self.tracker.wait(1)

    def wait_and_get_user_message(self):
        for _ in range(40):
            text = self.get_last_msg()
            if not re.search('bot\n',text,re.IGNORECASE):
                return text
            self.tracker.wait(1)

    def is_question(self,text=''):
        return bool(re.search(r"-->",text,flags=re.IGNORECASE))

    def get_answer(self,text=''):
        return re.findall(r'--> ([a-zA-Z0-9]+) <--',text)[0]

    def is_done(self,text=''):
        return bool(re.search(r'Congrats',text,flags=re.IGNORECASE))
    

if __name__ == '__main__':
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18513226'
    
    browser = None
    
    
    for _ in range(5):
        try:
            browser = SolveTyping(username_1, password_1,room_link)
            break
        except:
            print("no internet conenction,re-trying...")
            continue
    
    
    if browser:browser.driver.quit()