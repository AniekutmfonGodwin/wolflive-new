from dataclasses import dataclass,field
import re
from main import *
from strategies.exceptions import StopBotError
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
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except StopBotError:
                    raise StopBotError
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:
                    self.main()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
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
        else:
            self.toggle_autoplay()


    
    def check_autoplay_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().check_autoplay_status()")
        self.send_msg('!typing autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay .* (ON|OFF)',response,re.I)
        if res:
            return res[0]
        else:
            False
        

    def toggle_autoplay(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().toggle_autoplay()")
        self.send_msg('!typing autoplay')
        self.wait_and_get_user_message()


    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        for _ in range(40):
            try:
                if self.autoplay:
                    if not self.game_start:
                        self.send_msg('!typing')
                else:
                    self.send_msg('!typing')
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except StopBotError:
                raise StopBotError
            except Exception as e:

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
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_bot_message()")
        for _ in range(40):
            text = self.get_last_element().text
            if re.search('bot\n',text,re.IGNORECASE):
                return text
            self.tracker.wait(1)

    def wait_and_get_user_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_user_message()")
        for _ in range(40):
            text = self.get_last_element().text
            if not re.search('bot\n',text,re.IGNORECASE):
                return text
            self.tracker.wait(1)

    def is_question(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        return bool(re.search(r"-->",text,flags=re.IGNORECASE))

    def get_answer(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        return re.findall(r'--> ([a-zA-Z0-9]+) <--',text)[0]

    def is_done(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        return bool(re.search(r'Congrats',text,flags=re.IGNORECASE))



def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    
    browser = None
    
    
    for _ in range(5):
        try:
            browser = SolveTyping(username_1, password_1,room_link)
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
    room_link = 'https://wolf.live/g/18900545'
    
    browser = None
    
    
    for _ in range(5):
        try:
            return SolveTyping(username_1, password_1,room_link)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    # if browser:browser.driver.quit() 

    

if __name__ == '__main__':
    main()