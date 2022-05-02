from dataclasses import dataclass
import re
from time import sleep
from main import *
from strategies.exceptions import SignalRestartError, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
import sys


@dataclass
class WebDriver(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str

    def __post_init__(self):
        self.login()

##############################################
############ NUMBER DETECTIVE ################
##############################################

class SolveNumberDetective:
    loop_count:int = int()
    def __init__(self,browser1,browser2,test=False,loop_count:int=int):
        self.test = test
        self.browser1:WebDriver = browser1
        self.browser2:WebDriver = browser2
        self.browser = [self.browser1,self.browser2]
        self.turn = 0
        self.high = 100
        self.low = 0
        self.guess_number = 50
        self.high_keyword = [
           'is huge',
           'too high',
           'come down to earth',
           'is too big',
           'too much'
           
        ]
        self.low_keyword = [
            'is_tiny',
            'falls short',
            'think bigger',
            'the worst',
            'is low',
            'too low'
            

        ]
        self.loop_count:int = loop_count
        if not self.test:self.restart()

        

    def restart(self):
        self.loop_count = self.loop_count or int(input("How many time should i play the game e.g 10:\n") or 10)
        for _ in range(self.loop_count):
            self.loop_count -=1
            try:
                self.reset()
                self.main()
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except StopBotError:
                raise StopBotError
            except Exception as e:
                print("error occurred\n",e)
        raise StopBotError


    def close(self):
        try:
            self.browser1.close()
            self.browser2.close()
        except:
            pass
        
    
    def reset(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().reset()")
        self.turn = 0
        self.high = 100
        self.low = 0
        self.guess_number = 50

    

    
    def is_clue(self)->bool:
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_clue()")
        """
        takes in a text and return true if its a clue from the game bot
        parameters:
            text(str)
        return:
            True or False
        """
        return 'Follow this clue' in self.browser1.get_last_msg()

    def detector(self,direction:str='unknown')->dict:
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().detector()")
        if direction.lower() == 'high':
            self.high = self.guess_number
            self.guess_number = int((self.low+self.guess_number)/2)
        if direction.lower() == 'low':
            self.low =  self.guess_number
            self.guess_number = int((self.high+self.guess_number)/2)
        return self.guess_number
        

    def is_either_clue(self,text:str='')->bool:
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_either_clue()")
        return 'Follow this clue: Either' in text 

    def get_either_values(self,clue_text:str='')->list:
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_either_values()")
        return [int(x) for x in re.compile(r'[0-9]+').findall(clue_text)]

    def is_game_over(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_game_over()")
        return 'The trail went cold!' in self.browser1.get_last_bot_msg()

    def is_done(self)->bool:
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        return 'Congratulations' in self.browser1.get_last_bot_msg()

    
    def wait_and_get_question(self,loop=100):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_question()")
        """
            function pause any action until game start
            parameter:
                takes in browser objects
        """
        for _ in range(loop):
            text = self.browser1.get_last_msg()
            if 'Help me find a number' in text or 'Game already started! Follow' in text:
                return text
            self.browser1.tracker.wait(0.2)

    

    def get_bot_message(self,loop=100):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_bot_message()")
        """
            function pause all action till bot send a message
            parameters:
                broswer instance
            return:
                bot_message(str)
        """
        for count in range(loop):
            text =self.browser1.get_last_element().text
            if 'Number Detectives Bot'.lower() in text.lower():
                return text
            self.browser1.tracker.wait(0.2)
            self.browser1.tracker.signal_restart(count*0.2)

    def get_user_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_user_message()")
        """
            function pause any action untill a user sends a message
            parameter:
                browser instace
            return:
                user message(str)
        """
        for count in range(40):
            text =self.browser1.get_last_msg()
            if 'Number Detectives Bot' not in text:
                return text
            self.browser1.tracker.wait(1)
            self.browser1.tracker.signal_restart(count*1)


    def rotate_turn(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().rotate_turn()")
        self.turn = int(not self.turn)



    def get_clue(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_clue()")
        """
            this function return high or low depending on 
            the information contained in the clue
        """
        # clue = re.compile(r'Follow this clue: .+\n*').findall(self.browser1.get_last_msg())[0]
        # clue_text = ' '.join(clue.split()[3:])
        return self.low_or_high()
        # try:
            
        # except Exception as e:
        #     print("error:!!!!!",e)
        #     return False

    def low_or_high(self)->str:#not use function after the first guess
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().low_or_high()")
        text = self.browser1.get_last_msg()
        if re.findall(fr"{'|'.join(self.high_keyword)}",text,re.I):
            print("found in high")
            return 'high'

        if re.findall(fr"{'|'.join(self.low_keyword)}",text,re.I):
            print("found in low")
            return 'low'
        return 'unknown'

    

    # main(browser1)
    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        
        while True:
            try:
                self.browser1.send_msg('!nd')
                self.browser1.wait_for_bot_group()
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

        self.wait_and_get_question()
        self.browser[self.turn].send_msg(str(self.guess_number))
        self.rotate_turn()
        self.get_user_message()
        self.get_bot_message()

        while True:
            
            if self.is_clue():
                clue = self.get_clue()
                if clue:
                    new_guess = self.detector(clue)
                    print("new guess",new_guess)
                    self.browser[self.turn].send_msg(str(self.guess_number))
                    self.rotate_turn()
                    self.get_user_message()
                    self.get_bot_message()
                    self.browser1.tracker.reset()
            print("high",self.high,"low",self.low)
            if self.is_game_over():
                print("gameover")
                self.reset()
                break
            if self.is_done():
                print("congratulation")
                self.reset()
                break
            
            if self.high == 1+ self.low or self.high ==  self.low -1:
                print("is hooked")
                self.browser1.tracker.wait(40)




def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    # from games_bot import WebDriver

    SolveNumberDetective.loop_count = int(input("How many time should i play the game e.g 10:\n") or 10)

    browser = None
    browser2 = None
    nd:SolveNumberDetective = None

    for _ in range(20):
        try:
            if not browser:
                browser = WebDriver(username_1, password_1,room_link)
            if not browser2:
                browser2 = WebDriver(username_2, password_2,room_link)
            
            sleep(5)
            
            SolveNumberDetective(browser,browser2,loop_count=getattr(SolveNumberDetective,"loop_count",0))
            
         
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveNumberDetective.loop_count +=1

            continue
        except Exception as e:
            print("no internet conenction,re-trying...\n",e)
            continue
    
    if browser:browser.driver.quit()
    if browser2:browser2.driver.quit()
      


def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    # from games_bot import WebDriver

    SolveNumberDetective.loop_count = int(input("How many time should i play the game e.g 10:\n") or 10)

    browser = None
    browser2 = None
    nd:SolveNumberDetective = None

    for _ in range(20):
        try:
            if not browser:
                browser = WebDriver(username_1, password_1,room_link)
            if not browser2:
                browser2 = WebDriver(username_2, password_2,room_link)
            
            sleep(5)
            
            return SolveNumberDetective(browser,browser2,test=True,loop_count=getattr(SolveNumberDetective,"loop_count",0))
            
         
        except KeyboardInterrupt:
            break
        
        except SignalRestartError:
            SolveNumberDetective.loop_count +=1

            continue
        except Exception as e:
            print("no internet conenction,re-trying...\n",e)
            continue
    
    if browser:browser.driver.quit()
    if browser2:browser2.driver.quit()
        




if __name__ == '__main__' and "-i" not in sys.argv:
    main()
        
        