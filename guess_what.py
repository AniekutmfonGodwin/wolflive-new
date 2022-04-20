# %%
from dataclasses import dataclass,field
import re
from typing import List, Optional
from strategies.exceptions import StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from main import *
from time import sleep
import configparser
config = configparser.ConfigParser()
from utilities import search_image_by_google,search_image_by_bing

config.read('config.ini')








# %%
@dataclass
class Guesswhat(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    search_image:callable
    room_link:Optional[str] = 'https://wolf.live/g/18900545'
    search_url:Optional[str] = field(default_factory=lambda:'https://www.google.com/imghp?hl=en&tab=ri&ogbl')
    _category:Optional[str] = field(default_factory=str,init=False)
    image_code:Optional[str] = field(default_factory=lambda:None)
    image_url:Optional[str] = field(default_factory=lambda:None)
    guess:Optional[str] = field(default_factory=lambda:None)
    category:Optional[str] = field(default_factory=lambda:None)
    # Available Categories:
    # - Logos (ID 1)
    # - Close Ups (ID 2)
    # - Around The World (ID 3)
    # - Mixed (ID 4)
    # - Celebrities (ID 5)
    # - Sports (ID 6)
    # - Food (ID 7)
    # - Music (ID 8)
    # - Anime (ID 9)
    # - Nature (ID 10)
    # - 4in1 (ID 11)
    # - Shuffled (ID 13)
    

    def __post_init__(self):
        self.login()
        self.goto_group()
        self.check_autoplay('!gw autoplay','GuessWhat')
        self.tracker.wait(5)
        self.tracker.start()
        

    def login(self):
        res = super().login()
        self.driver.execute_script(f"window.open('{self.search_url}');")
        return res
        



    # state
    # -category

    # actions
    # -predict
    # start
    # -reset
    def start(self,category=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start()")
        command = None
        if self._category:
            command = f'!gw {self._category}'
            self.send_msg(command)
        else:
            command = f'!gw {category}'
            self.send_msg(command)
        for _ in range(10):
            if command.lower() in self.get_last_user_msg():break
            self.tracker.wait(1)
            

    def restart(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().restart()")
        self.start()

    def reset(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().reset()")
        self.image_code = None
        self.image_url = None
        self.guess = None
        self.category = None
        

    

    # events
    # on_question
    # on_game_over

    def on_question(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_question()")
        
        # if ele1.get_attribute("render-tag")=="palringo-chat-message-image" or ele2.get_attribute("render-tag")=="palringo-chat-message-image":
        if any([ele.get_attribute("render-tag")=="palringo-chat-message-image" for ele in self.get_latest_bot_msgs()[-2:]]):
            print("is question")
            self.tracker.reset(100)
            self.on_answer()
            
            # category:List[str] = re.findall(r"Category: (\w+)",self.get_last_bot_msg(index=-2),re.I)
            category:List[str] = re.findall(r"Category: (\w+)","".join([x.text for x in self.get_latest_bot_msgs()[-2:]]),re.I)

            if category:self.category = category[0].lower()

            # getting image source
            for ele in self.get_latest_bot_msgs()[-2:]:
                if ele.get_attribute("render-tag") == "palringo-chat-message-image":
                    if str(self.image_url) not in self.get_last_image_src(ele):
                        self.image_url = self.get_last_image_src(ele)
                        self._search()
                


    def _search(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}()._search()")
        qs = GuessWhat.objects.filter(image_code=self.image_code)
        if qs.exists():
            if qs.first().answer not in [None,'none','None',''] and all([self.image_code,self.image_url,self.category,self.guess]):
                self.send_msg(qs.first().answer)
                return ''
            
        data = re.findall(r'/production/(\d+)/',str(self.image_url),flags=re.IGNORECASE)
        if data:
            self.image_code = data[0]
        


        # search image with url
        for _ in range(50):
            try:
                self.goto_search()
                results = self.search_image(self.driver,url=self.image_url)
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except StopBotError:
                raise StopBotError
            except Exception as e:
                print(f"\n\n [{self.__class__}]{self.__class__.__name__}()._search({e})")
                self.driver.refresh()
                continue

        self.guess = '|'.join(results)
        print("\n\n guess ",self.guess)
        # searching image
        self.goto_group()
        for msg in results:
            self.tracker.wait(5)
            self.send_msg(msg)
        while not self.is_bot() and not self.is_stop():
            pass
        self.tracker.wait(2)



    def on_game_over(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_game_over()")
        if self.get_latest_bot_msgs()[-1].get_attribute("render-tag")!="palringo-chat-message-image":
            text = self.get_last_bot_msg()
            if re.findall(r"Game over",text,re.I) and all([self.image_code,self.image_url,self.category,self.guess]):
                print("\n\n is game over")
                data = {
                    "image_code":self.image_code,
                    "image_url":self.image_url,
                    "guess":self.guess,
                    "category":self.category
                }

                print("data",data)
                if not GuessWhat.objects.filter(image_code=self.image_code).exists():
                    GuessWhat.objects.create(**data)
                self.start()


    def on_answer(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_answer()")
        text = "\n".join([ele.text for ele in self.get_latest_bot_msgs()[-3:]])
        result = re.findall(r"Wow.+guessed it in .+ seconds!",text,re.I)
        if result and all([self.image_code,self.image_url,self.category,self.guess]):
            answer = self.get_last_user_msg()
            data = {
                    "image_code":self.image_code,
                    "image_url":self.image_url,
                    "answer":answer,
                    "category":self.category
                }
            qs = GuessWhat.objects.filter(image_code=self.image_code)
            if qs.exists():
                if not qs.first().answer:
                    qs.update(**data)
            else:
                GuessWhat.objects.create(**data)

            # reset properties
            self.reset()
            return data

    # utilities
    # -search_image
    # -get_image_src
    def get_last_image_src(self,ele):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_last_image_src()")
        return self.qs.action(".shadowRoot").getOne(".message-outer.layout")\
            .getOneShadowRoot('palringo-chat-message-image').getOne('#image-message').execute(ele).get_attribute('src')
            
   
        
    def goto_search(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().goto_search()")
        if len(self.driver.window_handles) < 2:
            self.driver.execute_script(f"window.open('{self.search_url}');")
        self.driver.switch_to.window(self.driver.window_handles[1])            
        
        



    
    


    


        
def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    search = None
    if config["Guesswhat"]["search_engine"] == "bing":
        search = search_image_by_bing
    else:
        search = search_image_by_google

    gw = Guesswhat(username_1,password_1,search,room_link = room_link)

    categories = [
        'Celebrities',
        'Logos',
        'Music',
        'Anime',
        'Close Ups',
        'Around The World',
        'Mixed',
        'Sports',
        'Food',
        'Nature',
        '4in1',
        'Shuffled'
    ]        
                
    # %%
    gw.start(categories[0])
    while True and not gw.is_stop():
        for category in categories[1:]:
            gw._category = category
            for _ in range(60001):
                gw.on_question()
                gw.on_game_over()
                if gw.is_stop():break

            if gw.is_stop():break


    gw.close()



def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    search = None
    if config["Guesswhat"]["search_engine"] == "bing":
        search = search_image_by_bing
    else:
        search = search_image_by_google

    return Guesswhat(username_1,password_1,search,room_link = room_link)

    # categories = [
    #     'Celebrities',
    #     'Logos',
    #     'Music',
    #     'Anime',
    #     'Close Ups',
    #     'Around The World',
    #     'Mixed',
    #     'Sports',
    #     'Food',
    #     'Nature',
    #     '4in1',
    #     'Shuffled'
    # ]        
                
    # %%
    # gw.start(categories[0])
    # while True and not gw.is_stop():
    #     for category in categories[1:]:
    #         gw._category = category
    #         for _ in range(60001):
    #             gw.on_question()
    #             gw.on_game_over()
    #             if gw.is_stop():break

    #         if gw.is_stop():break


    # gw.close()

        
     

# %%
if __name__ == '__main__':
    main()
# %%
# gw.get_last_user_msg(index=-2)
    
            
# %%
