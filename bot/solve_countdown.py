# %%
from dataclasses import dataclass,field
import re
from main import *
import main
from countdown_numbers_solver import get_expression_from_data
from time import sleep
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy







@dataclass
class SolveCountdown(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str
    category:str = field(default_factory=str)
    autoplay:bool = field(default_factory=bool,init=False)
    game_start:bool = field(default_factory=bool,init=False)
    stop:bool = field(default_factory=bool,init=False)

    def __post_init__(self):
        self.login()
        self.setup_status()
    
    def run(self):
        if self.autoplay:
            while True and not self.stop:
                try:
                    self.main()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt()
                except Exception as e:
                    print("error from main method\n",e)
                    continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                try:
                    if self.stop:break
                    self.main()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt()
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
        self.send_msg('!cd autoplay')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay is turned (ON|OFF)',str(response),re.I)
        if res:
            return res[0]
        else:
            False
        

    def toggle_autoplay(self):
        self.send_msg('!cd autoplay')
        self.tracker.wait(5)


    def is_stop_game(self):
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            self.driver.refresh()
            return

    def get_countdown_question_data(self,text=""):
        """
            return question data's if any or return false if non
        """
        try:
            data = re.split(r'using',re.findall(r'Calculate \d+ using .+\n*',text,re.I)[0],maxsplit=1)
            target = int(re.findall(r'\d+',data[0])[0])
            values = [int(x) for x in re.findall(r'\d+',data[1])]
            return {"target":target,"values":values}
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            return False

    def is_countdown_question(self,text=''):
        try:
            if re.search(r'Calculate',text,re.IGNORECASE):
                return text
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            return False

    def is_countdown_warning(self,text=''):
        return re.search(r"seconds remaining",text,re.IGNORECASE) and not re.search(r"The countdown has begun",text,re.IGNORECASE)
    def game_in_progress(self):
        return bool(re.findall(r"A game is already in progress|A game is about to begin",self.get_last_msg(),re.IGNORECASE))
    

    
    
    def render_number(self,data,ex,parttern=r'A'):
        """
            function insert number in expression
            parametr:
                data:list(int) #list of 6 integer item
                ex:str #string math equation
            return:
                string with digit inserted
                    
        """
        expression = ex
        for x in range(6):
            expression = re.sub(parttern,str(data[x]),expression,count=1)
        return expression


    def wait_and_get_bot_message(self):
        self.get_last_element()
        for _ in range(40):
            text = self.get_last_element().text
            if re.search('bot\n',text,re.IGNORECASE):
                return text
        sleep(1)

    def wait_and_get_user_message(self):
        for _ in range(40):
            text = self.get_last_element().text
            if not re.search('bot\n',text,re.IGNORECASE):
                return text
        sleep(1)


    def is_gameover(self):
        return bool(re.search(r'No winner',self.get_last_msg(),flags=re.IGNORECASE))

    def is_done(self):
        return bool(re.search(r'We have a winner',self.get_last_msg(),flags=re.IGNORECASE))


    def main(self):
        while True:
            try:
                if self.autoplay:
                    if not self.game_start:
                        self.send_msg('!cd')
                        self.game_start = True
                else:
                    self.send_msg('!cd')
                    self.game_start = True

                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except:
                continue
        

        while True:
            print("game start\nwaiting for bot")
            text = self.wait_and_get_bot_message()
            if self.is_gameover():
                print("game over")
                self.game_start = False
                break
            if self.game_in_progress():
                print("game in progress")
                self.game_start = True
            if self.is_done():
                print("congratulation")
                break
            if self.is_countdown_question(text=text):
                question_data = self.get_countdown_question_data(text=text)
                print("question data",question_data)
                # {"target":target,"values":values}
                if question_data:
                    expression = get_expression_from_data(question_data['target'],question_data['values'])
                    if expression:
                        self.send_msg(expression)
            
            if self.is_stop_game():
                print("you stoped the game")
                self.stop = True
                break

def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    # username_2 = 'Telek@gmail.com'
    # password_2 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    sc:SolveCountdown = None
    for _ in range(5):
        try:
            sc = SolveCountdown(username_1, password_1,room_link)
            sc.run()
            break
        except KeyboardInterrupt:
            print("interrupt")
            break
        except:
            print("no internet conenction,re-trying...")
            continue
    
    
    if sc:sc.tracker.wait(2)
    if sc:sc.close()
        
if __name__ == '__main__':
    main()

# %%
# main()
        
            
            
        
# %%
