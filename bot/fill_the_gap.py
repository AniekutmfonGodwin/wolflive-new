from dataclasses import dataclass,field
import re
from main import *
from typing import Any, Dict, Optional
import requests
from bs4 import BeautifulSoup
from time import sleep
from game.models import Gap
from strategies.exceptions import StopBotError
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
class SolveFillTheGap(
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
    
    def restart(self):
        return self.run()

    def run(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().run()")
        self.tracker.start()
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
            for _ in range(int(input("how many times do you want to play the game?\ne.g 200\n===>") or 200)):
                    if self.stop:break
                    self.main()
                # try:
                    
                # except Exception as e:
                #     print("refreashing browser",e)
                #     self.browser.driver.refresh()
                #     sleep(5)
        
        
    def get_answer(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        try:
            data = self.get_latest_msgs().execute()[-3].text
            if data:
                return re.findall(r'([a-zA-Z]+)',data)[0]
        except StopBotError:
            raise StopBotError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().get_answer({e})")



    def setup_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().setup_status()")
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
        
        


    
    def check_autoplay_status(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().check_autoplay_status()")
        """method check for the current autoplay status"""
        self.send_msg('!gap autoplay Music')
        self.wait_for_message_group('!gap autoplay Music')
        response = self.wait_for_bot_group()
        res =  re.findall(r'Autoplay .* (On|Off)',response,re.I)
        if res:
            return res[0]
        else:
            False
        

    def toggle_autoplay(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().toggle_autoplay()")
        """method toggle autoplay"""
        command = None
        if self.category:
            command = f'!gap autoplay {self.category}'
            self.send_msg(command)
        else:
            command = f'!gap autoplay'
            self.send_msg(command)
        self.wait_for_message_group(command)


    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        """the loop"""
        self.start_game()
        while True:
            if self.is_done():
                # self.update_workspace(answer=self.locate_answer())
                
                print("\n\n we've got a winner")
                _answer = self.get_answer()
                _question = self.workspace.get("question")
                if  Gap.objects.filter(question=self.workspace.get("question"),category=self.workspace.get("category").lower()).exists():
                    gp:Gap = Gap.objects.get(question =_question)
                    gp.answer = _answer
                    gp.save()
                    print("\n\n answer saved")

                # if _question and not Gap.objects.filter(question=_question).exists():
                #     Gap.objects.create(question=_question,answer=_answer,category=self.workspace.get("category").lower())
                
                self.tracker.wait(1)
                self.drop_workspace()
                self.tracker.wait(1)
                self.start_game()

            

            if self.is_question():
                self.tracker.reset()
                self.drop_workspace()
                print("\n\n is question")
                __question = self.get_question()
                category = self.get_category()
                self.update_workspace(question=__question,category=category)
                if self.workspace.get("question"):

                    
                    __answer =  self.predict(self.workspace.get("question"))
                    # print("created",self.workspace)

                    if __answer and not self.is_gameover():
                        self.send_msg(__answer)
                        print("\n\n answer is :",__answer)

                        # save to database
                        if not Gap.objects.filter(question=self.workspace.get("question")).exists():
                            Gap.objects.create(
                                question = self.workspace.get("question"),
                                guess = __answer,
                                category=self.workspace.get("category").lower()
                            )

                    self.wait_for_bot_group()

            



            if self.is_gameover():
                print("\n\n game over")
                self.game_start = False
                # print("droped",self.workspace)
                break

            
               



            if self.is_stop_game():
                print("\n\n you stoped the game")
                if self.workspace.get("timer"):self.workspace.get("timer").cancel()
                self.drop_workspace()
                self.stop = True
                break
                


    

    def start_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game()")
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
            except StopBotError:
                raise StopBotError
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().start_game({e})")
                continue

    def start_game_by_pass(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game_by_pass()")
        for _ in range(10):
            try:
                print("start game from thread")
                if self.category:
                    self.send_msg(f'!gap {self.category}')
                else:
                    self.send_msg('!gap')
                self.game_start = True
                break
            except StopBotError:
                raise StopBotError
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().start_game_by_pass({e})")
                continue
            


    



    def is_stop_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game()")
        try:
            return bool(re.findall(r'!stop',self.get_last_element().text,flags=re.IGNORECASE))
        except StopBotError:
            raise StopBotError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().is_stop_game({e}) ")
            self.driver.refresh()
            return

    


    def is_bot(self):
        try:
            super().is_bot()
        except StopBotError:
            raise StopBotError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().is_bot({e})")
            self.driver.refresh()
            return

    

    def is_question(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        return bool(re.search(r".*_ _ _ _.*",self.get_last_msg(),flags=re.IGNORECASE))

    def get_question(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_question()")
        try:
            return re.findall(r".*_ _ _ _.*\n*",self.get_last_msg(),flags=re.IGNORECASE)[0]
        except StopBotError:
            raise StopBotError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().get_question({e})")
            return False

    def get_category(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_category()")
        try:
            return re.findall(r"category: ([a-zA-Z]+)",self.get_last_msg(),flags=re.IGNORECASE)[0]
        except StopBotError:
            raise StopBotError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_category({e}) error")
            return False

    def is_gameover(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_gameover()")
        return bool(re.search(r'game over',self.get_last_msg(),flags=re.IGNORECASE))

    def is_done(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        text = "".join([x.text for x in self.get_latest_msgs().execute()[-2:]])
        return bool(re.search(r'Here are the winners',text,flags=re.IGNORECASE))
        

    def is_web_bot_protection(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_web_bot_protection()")
        return bool(re.search(r'Our systems have detected unusual traffic from your computer network',text,flags=re.IGNORECASE))



    


    def predict(self,question):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().predict()")
        try:
            
            # check from database
            if question and Gap.objects.filter(question=question).exists():
                gap = Gap.objects.get(question=question)
                if gap.answer:
                    print(f"\n\n [{self.__class__}]{self.__class__.__name__}().predict({gap.answer.strip()}) running from database")
                    return gap.answer.strip()

            if question:
                print(f"\n\n [{self.__class__}]{self.__class__.__name__}().predict() using request")
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
                            print(f"\n\n [{self.__class__}]{self.__class__.__name__}().predict({answer.strip()}) using request")
                            return answer.strip()
        except StopBotError:
            raise StopBotError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(f"\n\n error \n\n [{self.__class__}]{self.__class__.__name__}().predict({e})")
            return None
        

def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    
    s:SolveFillTheGap = None
    for _ in range(5):
        try:
            s = SolveFillTheGap(username_1, password_1,room_link)
            s.run()
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except StopBotError:
            raise StopBotError()
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            if s:s.close()
            continue
    
    sleep(2)
    s.close()



if __name__ == '__main__':
    main()
        
        
    

    
            
        
        

