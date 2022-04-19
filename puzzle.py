# %%
from dataclasses import dataclass,field
from email.policy import default
from typing import List, Optional
from strategies.exceptions import StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from bs4 import BeautifulSoup
from main import *
import configparser

import logging
from selenium.common.exceptions import StaleElementReferenceException



config = configparser.ConfigParser()
config.read('config.ini')




logger = logging.getLogger()
logger.setLevel(logging.DEBUG)






@dataclass
class Puzzle(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:Optional[str] = 'https://wolf.live/g/18900545'
    private_url:Optional[str] ='https://wolf.live/u/80277459'
    moves:List[str] = field(default=list)
    remaining_puzzle:List[str] = field(default=list)
    image_links:List[str] = field(default=list)
    stop_on_user:List[str] = field(default=False)
    stop_play_loop:List[str] = field(default=False)
    stop_loop:List[str] = field(default=False)

    def __post_init__(self):
        self.login()
        self.reset_moves()

    # def __init__(self,username,password,room_link=None):
    #     super().__init__(username,password,room_link=room_link)
    #     self.moves = list()
    #     self.remaining_puzzle = list()
    #     self.image_links = dict()

    #     self.stop_on_user = False
    #     self.stop_play_loop = False
    #     self.stop_loop = False


    #     self.reset_moves()
      




    def restart(self):
        self.login()
        self.run()
    

 


    def play(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().play()")
        if self.is_debug:print(f"\n\n [{self.__class__}]{self.__class__.__name__}().play()")
        self.remaining_puzzle = self.get_puzzle_number()
        if not self.remaining_puzzle:return
        start_position = self.remaining_puzzle[0]
        end_position = 0
        while self.remaining_puzzle == self.get_puzzle_number() and not self.is_stop():
            end_position = end_position + 1
            try:
                self.move_tiles(f"{start_position} {self.remaining_puzzle[end_position]}")
                
            except:break
            for _ in range(10):
                if self.is_image_msg() and not self.is_stop():break
                print("waiting for bot message")





    # task
    def start_game(self,difficulty='',*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game(difficulty={difficulty},{args},{kwargs})")
        self.stop_on_user = False
        self.stop_loop = False
        logger.info("start game")
        print("start game")
        self.send_msg(f"!puzzle start {difficulty}")


    def end_game(self,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().end_game({args},{kwargs})")
        self.stop_on_user = True
        self.stop_loop = True
        logger.info("ended game")
        print("ended game")
        self.send_msg("!puzzle end")

    def get_frame_element(self,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_frame_element({args},{kwargs})")
        element = self.get_last_puzzle_question()[-1]
        return self.qs.action(".shadowRoot").getOneShadowRoot("palringo-chat-message-pack").getOne("#content").execute(element)


    def get_puzzle_number(self,element=None,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_puzzle_number(element={element},{args},{kwargs})")
        logger.info("get puzzle number")
        print("get puzzle number")
        
        element = element or self.get_frame_element()
        
        self.driver.switch_to.frame(element)
        
        content = self.driver.page_source
        
        self.driver.switch_to.default_content()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # scramble image
        tables = soup.select("table.puzzle-mp-puzzle__content__page__puzzle")
        
        numbers_element = tables[0].select(".puzzle-mp-puzzle__content__page__puzzle__row__tile__number")
        
        return [int(x.text) for x in numbers_element]
        

        



    

    def move_tiles(self,moves:str='',*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().move_titles()")
        logger.info("move tile:moves -> "+moves)
        print("move tile:moves -> "+moves)
        self.send_msg(str(moves))
        self.tracker.wait(3)
        


    def get_last_puzzle_question(self,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_puzzle_question()")
        return [x for x in self.get_latest_msgs().execute() if x.get_attribute("is-bot")=='' and x.get_attribute("render-tag") in 'palringo-chat-message-pack']
        

    def reset_moves(self,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().reset_moves()")
        logger.info("reset moves")
        print("reset moves")
        config["Puzzle"]["moves"] = ""
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


    
    def is_image_msg(self,index=-1,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_image_msg()")
        element_selenium = self.get_latest_bot_msgs()
        if not element_selenium:return False
        element = element_selenium[index]
        return element.get_attribute("is-bot")=='' and 'palringo-chat-message-pack' in element.get_attribute("render-tag")
        


    # event

    def on_question(self,func=None,negate=False,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_question()")
        condition = 'The group has 60 minutes to solve this puzzle!' in self.get_last_bot_msg(index=-2)
        
        if self.is_image_msg() and condition:
            logger.info("on question")
            print("on question")
            func(*args,**kwargs) if func else print("on question")
        else:
            if negate:
                 func(*args,**kwargs) if func else print("not on question")

    

    def on_already_a_game(self,func:Optional[callable]=None,negate=False,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_already_a_game({func},{negate},{args},{kwargs})")
        
        message = self.get_last_bot_msg(index=-2)
        condition = "There's already an active puzzle in this group" in message
        
        if self.is_image_msg() and condition:
            logger.info("on already a game")
            print("on already a game")
            func(*args,**kwargs) if func else print("on_already_a_message")
        else:
            if negate:
                func(*args,**kwargs) if func else print("not on_already_a_message")
        

    def on_fail(self,func=None,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_fail()")
        if not self.is_image_msg() and 'The group failed to solve the puzzle within an hour' in self.get_last_bot_msg():
            print("on_fail")
            func(*args,**kwargs) if func else print("on_fail")

    def on_warning(self,func=None,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_warning()")
        if not self.is_image_msg() and 'The group has 10 minutes remaining to solve the puzzle' in self.get_last_bot_msg():
            func(*args,**kwargs) if func else print("on_warning")



    def on_success(self,func=None,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_success()")
        # if not self.is_image_msg(index=-3) and 'The puzzle was completed in' in self.get_last_bot_msg(index=-3):
        if any([
            'The puzzle was completed in' in self.get_last_bot_msg(index=-3),
            'The puzzle was completed in' in self.get_last_bot_msg(index=-2),
            'The puzzle was completed in' in self.get_last_bot_msg(index=-1),
        ]):
            func(*args,**kwargs) if func else print("on_success")

        # save image links and moves to database

    

    def run(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().run()")
        self.on_question(func=self.start_game,negate =True,difficulty=config["Puzzle"]["difficulty"])
        logger.info("game start")
        print("game start")
        
        for _ in range(5):
            if self.is_bot() and self.is_image_msg() and not self.is_stop():break
            print("waiting for bot message")
            self.tracker.wait(seconds=1)

        def from_db(*args, **kwargs):
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}().from_db()")
            self.stop_play_loop = False
            def stop_loop(*args, **kwargs):
                self.stop_play_loop = True
            while not self.stop_play_loop and not self.is_stop():
                self.play()
                self.on_success(func=stop_loop)
         

        def stop():
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}().stop()")
            self.reset_moves()
            self.stop_loop = True
            self.stop_on_user = True

        
        logger.info("main loop start")
        print("main loop start")
        while not self.stop_loop and not self.is_stop():
            self.on_already_a_game(func=from_db)
            self.on_question(func=from_db)
            self.on_fail(func=stop)
            self.on_success(func=self.start_game)

        logger.info("main loop stop")
        print("main loop stop")

def main():
    room_link = 'https://wolf.live/g/18900545'
    private_url ='https://wolf.live/u/80277459'
    username = 'Komp@gmail.com'
    password = '123456'
    puzzle = Puzzle(username,password,room_link,private_url)
    for _ in range(100):
        try:
            puzzle.run()
        except KeyboardInterrupt:
            raise KeyboardInterrupt("stop bot keyboard command")
        except StopBotError:
            raise StopBotError("stop bot bot command")
        except StaleElementReferenceException:
            print("element not attach to the dom,refreshing")
            if puzzle.driver:puzzle.driver.refresh()
        puzzle.tracker.wait(seconds=3)


# %%
if __name__ == '__main__':
    main()
    

    

