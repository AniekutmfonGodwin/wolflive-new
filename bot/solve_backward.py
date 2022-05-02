from dataclasses import dataclass,field
import re
import sys
from main import *
from strategies.exceptions import SignalRestartError, StopBotError
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
    loop_count:int = field(default_factory=int)
    test:bool = field(default_factory=bool)
    def __post_init__(self):
        self.login()
        self.setup_status()
        if not self.test:self.restart()
        


    def restart(self):
        if not self.is_login:self.update_driver()
        if self.autoplay:
            while True and not self.stop:
                try:
                    self.main()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except StopBotError:
                    raise StopBotError
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(self.loop_count or int(input("how many times do you want to play the game?\ne.g 200\n===>") or 200)):
                try:

                    if self.stop:break
                    self.main()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except StopBotError:
                    raise StopBotError
                except Exception as e:
                    print("error from main method\n",e)

            raise StopBotError


    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
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
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except StopBotError:
                raise StopBotError
            except Exception as e:
                print(e)
                continue

        while True:
            try:
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
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except StopBotError:
                raise StopBotError
            except Exception as e:
                raise Exception
            

    

    def setup_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().setup_status()")
        if str(input("play game with auto mood (yes/no):\n===>")).lower() == 'yes':
            self.autoplay = True
        status:str = self.check_autoplay_status()
        if status.upper()=='ON':
            if not self.autoplay:
                self.toggle_autoplay()
        elif status.upper()=='OFF':
            if self.autoplay:
                self.toggle_autoplay()
        else:
            self.toggle_autoplay()
    
    def check_autoplay_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().check_autoplay_status()")
        self.send_msg('!backwards autoplay')
        self.wait_for_message_group('!backwards autoplay')
        response = self.wait_for_bot_group()
        res =  re.findall(r"Autoplay is now turned (ON|OFF)",response,re.I)
        print("result from regex",res)
        if res:
            return res[0]
        else:
            raise Exception("site features has change update bot")
            # return False
        
    def toggle_autoplay(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().toggle_autoplay()")
        self.send_msg('!backwards autoplay')

    def is_stop_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game()")
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except SignalRestartError:
            self.close()
            raise SignalRestartError
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print(e)
            self.driver.refresh()
            return

    def is_question(self,text):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question(text={text})")
        return bool(re.search(r"-->",text,flags=re.IGNORECASE))
            

    def get_answer(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer(text={text})")
        return re.findall(r'--> ([a-zA-Z0-9]+) <--',text)[0][::-1]


    def is_done(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done(text={text})")
        return bool(re.search(r'Congrats',text,flags=re.IGNORECASE))
        

    



    

def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    # username_2 = 'Telek@gmail.com'
    # password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    
    s:SolveBackward = None
    SolveBackward.loop_count = int(input("how many times do you want to play the game?\ne.g 200\n===>") or 200)
    
    for _ in range(10):
        try:
            s = SolveBackward(username_1, password_1,room_link,loop_count=getattr(SolveBackward,"loop_count",0))
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except SignalRestartError:
            SolveBackward.loop_count = s.loop_count
            continue
        except StopBotError:
            raise StopBotError
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    
    if s:s.tracker.wait(2)
    
    if s:s.close()

if __name__ == '__main__' and not sys.argv[1]:
    main()