from dataclasses import dataclass,field
from time import sleep
import re
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy


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

    def __post_init__(self):
        self.login()
        self.setup_status()
        if self.autoplay:
            while True and not self.stop:
                try:
                    self.main()
                except Exception as e:
                    print("error from main method\n")
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:
                    if self.stop:break
                    self.main()
                except:
                    continue
                    

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
        self.send_msg('!math autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay is turned (ON|OFF)',response,re.I)
        if res:
            return res[0]
        else:
            False
        

    def toggle_autoplay(self):
        self.send_msg('!math autoplay')
        self.wait_and_get_user_message()


    def start_game(self):
        for _ in range(10):
            if not self.game_start:
                try:
                    self.send_msg('!math')
                    self.game_start = True
                    break
                except:
                    sleep(1)
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
            text = self.wait_and_get_bot_message()
            if self.is_question(text):
                answer =  self.get_answer(text=text)

                if answer:
                    self.send_msg(answer)
                    # print("answer is :",answer)

            if self.is_done(text):
                # print("we have a winner\n",text)
                break
            if self.is_stop_game():
                self.stop = True
                break

            if self.is_gameover():
                self.game_start = False
                break



    def wait_and_get_bot_message(self):
        for _ in range(40):
            text = self.get_last_element().text
            if re.search('bot\n',text,re.IGNORECASE):
                return text
            
            

    def wait_and_get_user_message(self):
        for _ in range(40):
            text = self.get_last_element().text
            if not re.search('bot\n',text,re.IGNORECASE):
                return text

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
    
    for _ in range(5):
        try:
            browser = SolveMathsBot(username_1, password_1,room_link)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        # except Exception as e:
        #     print("no internet conenction,re-trying...",e)
        #     continue
    
    
    if browser:browser.close()


if __name__ == '__main__':
    main()
    
    