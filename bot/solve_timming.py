from dataclasses import dataclass,field
import re
from main import *
from strategies.exceptions import StopBotError
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
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        if self.options == '1':self.start_game()
        while True:
            # text = self.wait_and_get_bot_message()
            if self.is_question():
                answer =  self.get_answer()
                print("\n\n answer\nإجابة",answer)
                if answer:
                    self.tracker.wait(float(answer[1])-1.4)
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
                break

            if self.is_done():
                print("we have a winner\nلدينا فائز")
                break


    def wait_and_get_bot_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_bot_message()")
        while True:
            text = self.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text

    def is_question(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        return bool(re.search(r"لعبة فردية:",self.get_last_msg(),flags=re.IGNORECASE))

    def get_answer(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        return re.findall(r'\{(.+)\} بعد مرور (\d+) ثانية',self.get_last_msg())[0]
        

    

    def is_gameover(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_gameover()")
        return bool(re.search(r'انتهت اللعبة',self.get_last_msg(),flags=re.IGNORECASE))
        

    def is_done(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        return bool(re.search(r'الفائز',self.get_last_msg(),flags=re.IGNORECASE))
        

    def is_stop_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game()")
        try:
            return bool(re.findall(r'قف!|!stop|!قف',self.get_last_msg(),flags=re.IGNORECASE))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except Exception as e:
            self.driver.refresh()
            print(f"\n\n error\n\n[{self.__class__}]{self.__class__.__name__}().is_stop_game({e})")
            return

    def start_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game()")
        for _ in range(10):
            try:
                # self.browser.send_msg('!timing')
                self.send_msg('!وقت')
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except StopBotError:
                raise StopBotError
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
            browser = SolveTimming(username_1, password_1,room_link)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
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
            browser = SolveTimming(username_1, password_1,room_link)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    return browser
    # if browser:browser.driver.quit()
    
    
    

if __name__ == '__main__':
    main()


    


    # def answer_lyrics(self,question):