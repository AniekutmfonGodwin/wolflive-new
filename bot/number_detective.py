from dataclasses import dataclass
import re
from time import sleep
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy

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

class solve_number_detective:
    def __init__(self,browser1,browser2):
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

        for _ in range(int(input("How many time should i play the game e.g 10:\n"))):

            try:
                self.turn = 0
                self.high = 100
                self.low = 0
                self.guess_number = 50
                self.main()
            except Exception as e:
                print("error occurred\n",e)





    

    
    def is_clue(self)->bool:
        """
        takes in a text and return true if its a clue from the game bot
        parameters:
            text(str)
        return:
            True or False
        """
        return 'Follow this clue' in self.browser1.get_last_msg()

    def detector(self,direction:str='unknown')->dict:
        if direction.lower() == 'high':
            self.high = self.guess_number
            self.guess_number = int((self.low+self.guess_number)/2)
        if direction.lower() == 'low':
            self.low =  self.guess_number
            self.guess_number = int((self.high+self.guess_number)/2)
        return self.guess_number
        

    def is_either_clue(self,text:str='')->bool:
        return 'Follow this clue: Either' in text 

    def get_either_values(self,clue_text:str='')->list:
        return [int(x) for x in re.compile(r'[0-9]+').findall(clue_text)]
    def is_game_over(self):
        return 'The trail went cold!' in self.browser1.get_last_msg()

    def is_done(self)->bool:
        return 'Congratulations' in self.browser1.get_last_msg()

    
    def wait_and_get_question(self):
        """
            function pause any action until game start
            parameter:
                takes in browser objects
        """
        for _ in range(100):
            text = self.browser1.get_last_msg()
            if 'Help me find a number' in text or 'Game already started! Follow' in text:
                return text
            sleep(1)

    

    def get_bot_message(self):
        """
            function pause all action till bot send a message
            parameters:
                broswer instance
            return:
                bot_message(str)
        """
        for _ in range(40):
            text =self.browser1.get_last_msg()
            if 'Number Detectives Bot' in text:
                return text
            sleep(1)

    def get_user_message(self):
        """
            function pause any action untill a user sends a message
            parameter:
                browser instace
            return:
                user message(str)
        """
        for _ in range(40):
            text =self.browser1.get_last_msg()
            if 'Number Detectives Bot' not in text:
                return text
            sleep(1)

    def rotate_turn(self):
        self.turn = not self.turn



    def get_clue(self):
        """
            this function return high or low depending on 
            the information contained in the clue
        """
        clue = re.compile(r'Follow this clue: .+\n*').findall(self.browser1.get_last_msg())[0]
        clue_text = ' '.join(clue.split()[3:])
        return self.low_or_high()
        # try:
            
        # except Exception as e:
        #     print("error:!!!!!",e)
        #     return False

    def low_or_high(self)->str:#not use function after the first guess
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
        
        while True:
            try:
                self.browser1.send_msg('!nd')
                break
            except:
                continue

        self.wait_and_get_question()
        self.browser[self.turn].send_msg(str(self.guess_number))
        self.turn = not self.turn
        self.get_user_message()
        self.get_bot_message()
        for _ in range(20):
            if self.is_clue():
                clue = self.get_clue()
                if clue:
                    new_guess = self.detector(clue)
                    print("new guess",new_guess)
                    self.browser[self.turn].send_msg(str(self.guess_number))
                    self.turn = not self.turn
                    self.get_user_message()
                    self.get_bot_message()
            print("high",self.high,"low",self.low)
            if self.is_game_over():
                print("gameover")
                break
            if self.is_done():
                print("congratulation")
                break
            
            if self.high == 1+ self.low or self.high ==  self.low -1:
                print("is hooked")
                sleep(40)









if __name__ == '__main__':
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    username_2 = 'Telek@gmail.com'
    password_2 = '123456'
    room_link = 'https://wolf.live/g/18405280'
    # from games_bot import WebDriver

    

    browser = None
    browser2 = None
    is_login = False

    for _ in range(5):
        try:
            if not browser:
                browser = WebDriver(username_1, password_1,room_link)
            if not browser2:
                browser2 = WebDriver(username_2, password_2,room_link)
            is_login = True
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("no internet conenction,re-trying...\n",e)
            continue
    
    
    sleep(2)
    if is_login:    
        solve_number_detective(browser,browser2)
        browser.driver.quit()
        browser2.driver.quit()
    if browser:browser.driver.quit()
    if browser2:browser2.driver.quit()
        
        