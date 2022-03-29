from dataclasses import dataclass,field
import re
from typing import Any, Dict, Optional
import requests
from bs4 import BeautifulSoup
from time import sleep
from game.models import Gap
from main import *
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from workspace import workspace





# get_bot_message(broswer)
"""
    function waits untill bot send a message
"""

# is_gameover(text='')
"""
    function returns true if game is over
"""

# get_question(text="")

# is_question(text='')


# get_answer(question)

@dataclass
class solve_fill_the_gap(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy,
    workspace
    ):
    username:str
    password:str
    room_link:str
    category:str = field(default_factory=lambda:'Music')
    workspace:Dict[str,Any] = field(default_factory=dict)
    autoplay:Optional[bool] = field(default_factory=bool)
    game_start:Optional[bool] = field(default_factory=bool)
    stop:Optional[bool] = field(default_factory=bool)
    timer:Optional[Any] = field(default_factory=lambda:None)
    

    def __post_init__(self):
        self.login()
        self.workspace = {
            "question":None,
            "anwser":None,
            "category":self.category
        }
        # self.stop = False
        self.setup_workspace()
        self.tracker.wait(1)
        # self.timer = None

    


        # method setup auto play 
        self.setup_status()
        if self.autoplay:
            while True and not self.stop:
                    self.main()
                # try:
                # except:
                #     print("refreashing browser")
                #     self.browser.driver.refresh()
                #     sleep(5)
                #     continue
        else:
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>"))):
                    if self.stop:break
                    self.main()
                # try:
                    
                # except Exception as e:
                #     print("refreashing browser",e)
                #     self.browser.driver.refresh()
                #     sleep(5)
        
        
    def get_answer(self):
        try:
            data = self.get_latest_msgs().execute()[-3].text
            if data:
                return re.findall(r'([a-zA-Z]+)',data)[0]
            
        except:
            pass



    def setup_status(self):
        """method set autoplay mode"""
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
        """method check for the current autoplay status"""
        self.send_msg('!gap autoplay Music')
        self.wait_and_get_user_message()
        response = self.wait_and_get_bot_message()
        res =  re.findall(r'Autoplay is turned (ON|OFF)',response,re.I)
        if res:
            return res[0]
        else:
            False
        

    def toggle_autoplay(self):
        """method toggle autoplay"""
        if self.category:
            self.send_msg(f'!gap autoplay {self.category}')
        else:
            self.send_msg(f'!gap autoplay')
        self.wait_and_get_user_message()


    def main(self):
        """the loop"""
        self.start_game()
        while True:
            if self.is_done():
                # self.update_workspace(answer=self.locate_answer())
                
                print("we've got a winner")
                _answer = self.get_answer()
                _question = self.workspace.get("question")
                if  Gap.objects.filter(question=self.workspace.get("question"),category=self.workspace.get("category").lower()).exists():
                    gp = Gap.objects.get(question =_question)
                    gp.answer = _answer
                    gp.save()
                    print("answer saved")

                # if _question and not Gap.objects.filter(question=_question).exists():
                #     Gap.objects.create(question=_question,answer=_answer,category=self.workspace.get("category").lower())
                
                self.tracker.wait(1)
                self.drop_workspace()
                self.tracker.wait(1)
                # print("droped",self.workspace)

            # if self.is_bot():
            #     # timer code
            #     print("is bot")
            #     check_timer = self.timer
            #     if check_timer:check_timer.cancel()
            #     t=Timer(60.0,self.start_game_by_pass)
            #     self.timer = t
            #     t.start()

            if self.is_question():
                self.drop_workspace()
                print("is question")
                __question = self.get_question()
                category = self.get_category()
                self.update_workspace(question=__question,category=category)
                if self.workspace.get("question"):

                    
                    __answer =  self.predict(self.workspace.get("question"))
                    # print("created",self.workspace)

                    if __answer and not self.is_gameover():
                        self.send_msg(__answer)
                        print("answer is :",__answer)

                        # save to database
                        if not Gap.objects.filter(question=self.workspace.get("question")).exists():
                            Gap.objects.create(
                                question = self.workspace.get("question"),
                                guess = __answer,
                                category=self.workspace.get("category").lower()
                            )

                    self.wait_and_get_bot_message()

            



            if self.is_gameover():
                print("game over")
                self.game_start = False
                # print("droped",self.workspace)
                break

            
                



            if self.is_stop_game():
                print("you stoped the game")
                if self.workspace.get("timer"):self.workspace.get("timer").cancel()
                self.drop_workspace()
                self.stop = True
                break
                


    

    def start_game(self):
        for _ in range(10):
            try:
                if self.autoplay and not self.game_start:
                    if self.category:
                        self.send_msg(f'!gap {self.category}')
                    else:
                        self.send_msg('!gap')
                    self.game_start = True
                
                if not self.autoplay:
                    if self.category:
                        self.send_msg(f'!gap {self.category}')
                    else:
                        self.send_msg('!gap')
                    self.game_start = True
                break
            except:
                continue

    def start_game_by_pass(self):
        for _ in range(10):
            try:
                print("start game from thread")
                if self.category:
                    self.send_msg(f'!gap {self.category}')
                else:
                    self.send_msg('!gap')
                self.game_start = True
                break
            except:
                continue
            


    

    def wait_and_get_user_message(self):
        for _ in range(10):
            text = self.get_last_msg()
            if not re.search('bot\n',text,re.IGNORECASE):
                return text
        sleep(1)

    def is_stop_game(self):
        try:
            return bool(re.findall(r'!stop',self.get_last_msg(),flags=re.IGNORECASE))
        except:
            self.driver.refresh()
            return




    def is_bot(self):
        try:
            text = self.get_last_msg()
            if re.findall('bot\n',text,re.IGNORECASE):
                return text
        except:
            self.driver.refresh()
            return

    def wait_and_get_bot_message(self):
        for _ in range(10):
            text = self.get_last_msg()
            if re.search('bot\n',text,re.IGNORECASE):
                return text
            sleep(1)

    def is_question(self):
        return bool(re.search(r".*_ _ _ _.*",self.get_last_msg(),flags=re.IGNORECASE))

    def get_question(self):
        try:
            return re.findall(r".*_ _ _ _.*\n*",self.get_last_msg(),flags=re.IGNORECASE)[0]
        except:
            return False

    def get_category(self):
        try:
            return re.findall(r"category: ([a-zA-Z]+)",self.get_last_msg(),flags=re.IGNORECASE)[0]
        except:
            return False

    def is_gameover(self):
        return bool(re.search(r'game over',self.get_last_msg(),flags=re.IGNORECASE))

    def is_done(self):
        for x in self.get_latest_msgs()[-2:]:
            return bool(re.search(r'Here are the winners',x.text,flags=re.IGNORECASE))
        

    def is_web_bot_protection(self,text=''):
        return bool(re.search(r'Our systems have detected unusual traffic from your computer network',text,flags=re.IGNORECASE))



    


    def predict(self,question):

        try:
            
            # check from database
            if question and Gap.objects.filter(question=question).exists():
                gap = Gap.objects.get(question=question)
                if gap.answer:
                    print("running from database")
                    return gap.answer.strip()

            print("request")
            if question:


                url = 'https://www.lyrics.com/lyrics/'+ re.sub(r'[ ]*_[^,]+_[ ]*','',question)
                response = requests.get(url)
                soup = BeautifulSoup(response.content,'html.parser')
                lyrics = [x.text for x in soup.select('.lyric-body')]

                if len(lyrics):
                    
                    words = re.findall(r'[\b]?[a-zA-Z\']+[\b]?',question,flags=re.I)

                    pattern = r"\b"+r'|'.join(words)
                    # re.findall(pattern,question)

                    lyrics.sort(key = lambda x:-len(re.findall(pattern,x,flags=re.I)))
                    gap = re.findall(r"[\b]?[a-zA-Z ]{0,10}_[^,]+_[\b,]?[^_]?[a-zA-Z]{0,10}[\b]?",question,flags=re.I)[0]
                    
                    
                    pattern = re.sub(r'_[^,]+_[\b,]?[^_ ]?',f'[a-zA-Z0-9\']+',gap,flags=re.I)
                    
                    
                    for lyrics_one in lyrics:
                        answer_raw = re.findall(rf"{pattern}",lyrics_one,flags=re.I)
                        if len(answer_raw):

                            def check(x):
                                return x not in pattern_words

                            pattern_words = re.findall(r'[a-zA-Z0-9\']+',pattern)
                            answer_words = re.findall(r'[a-zA-Z0-9\']+',answer_raw[0])
                            answer = list(filter(check,answer_words))[0]

                            return answer.strip()
                        
        except:
            return None





if __name__ == '__main__':
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18477707'
    
    s:solve_fill_the_gap = None
    for _ in range(5):
        try:
            s = solve_fill_the_gap(username_1, password_1,room_link)
            break
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            if s:s.close()
            continue
    
    sleep(2)
    s.close()
        
        
    

    
            
        
        

