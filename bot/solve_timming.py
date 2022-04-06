from dataclasses import dataclass,field
import re
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy



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

    def __post_init__(self):
        self.login()
        self.options = input("choose an option\n1)bot start game\n2)user start game\n==> ")
        while True and not self.stop:
            try:
                self.main()
            except Exception as e:
                print("error occurred\n",e)

    def main(self):
        if self.options == '1':self.start_game()
        while True:
            # text = self.wait_and_get_bot_message()
            if self.is_question():
                answer =  self.get_answer()
                print("answer\nإجابة",answer)
                if answer:
                    self.tracker.wait(float(answer[1])-1.4)
                    if self.is_stop():
                        self.stop = True
                        print("stopped game")
                        break
                    self.send_msg(answer[0])


            if self.is_stop():
                self.stop = True
                print("stopped game")
                break

            if self.is_gameover():
                print("game over\nانتهت اللعبة")
                break

            if self.is_done():
                print("we have a winner\nلدينا فائز")
                break


    def wait_and_get_bot_message(self):
        while True:
            text = self.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text

    def is_question(self):
        # return bool(re.search(r"Single game",text,flags=re.IGNORECASE))
        return bool(re.search(r"لعبة فردية:",self.get_last_msg(),flags=re.IGNORECASE))

    def get_answer(self):
        return re.findall(r'\{(.+)\} بعد مرور (\d+) ثانية',self.get_last_msg())[0]
        # return re.findall(r'\{(.+)\} (\d+) seconds',text)[0]

    

    def is_gameover(self):
        return bool(re.search(r'انتهت اللعبة',self.get_last_msg(),flags=re.IGNORECASE))
        # return bool(re.search(r'game over',text,flags=re.IGNORECASE))

    def is_done(self):
        return bool(re.search(r'الفائز',self.get_last_msg(),flags=re.IGNORECASE))
        # return bool(re.search(r'winner',text,flags=re.IGNORECASE))

    def is_stop_game(self):
        try:
            # return bool(re.findall(r'!stop|قف!',self.browser.get_last_msg(),flags=re.IGNORECASE))
            return bool(re.findall(r'قف!|!stop|!قف',self.get_last_msg(),flags=re.IGNORECASE))
        except:
            self.driver.refresh()
            return

    def start_game(self):
        for _ in range(10):
            try:
                # self.browser.send_msg('!timing')
                self.send_msg('!وقت')
                break
            except:
                continue
        

    

if __name__ == '__main__':
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    
    browser = None
    
    for _ in range(5):
        try:
            browser = SolveTimming(username_1, password_1,room_link)
            break
        except KeyboardInterrupt:
            break
        except:
            print("no internet conenction,re-trying...")
            continue
    
    
    
    if browser:browser.driver.quit()


    


    # def answer_lyrics(self,question):