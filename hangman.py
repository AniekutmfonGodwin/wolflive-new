# %%
from dataclasses import dataclass,field
from typing import List, Optional
from strategies.exceptions import StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
import re
from time import sleep
import json
from random import choice
from main import *
from main import WordList,GuessWhat
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# %%
@dataclass
class Hangman(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    private_url:Optional[str] = field(default_factory=lambda:'https://wolf.live/u/80277459')
    room_link:Optional[str] = field(default_factory=lambda:'https://wolf.live/g/18900545')
    word_list:List[str] = field(default_factory=list)
    incorrect_letters:List[str] = field(default_factory=list)
    old_incorrect_letters:List[str] = field(default_factory=list)
    current_pattern:str = field(default_factory=str)
    word_count:int = field(default_factory=int)
    live:int = field(default_factory=int)
    starter_letters:List[str] = field(default_factory=lambda:[
            'e','t','a','o','i','n','s','h',
            'r','d','l','u','c','m','f','w','y',
            'p','v','b','g','k','q','j','x','z'
        ])
    
    

    def __post_init__(self):
        self.login()
        self.get_wordlist_from_source()


    """
    # state
    live
    guess_word
    incorrect_letter
    word_count
    word_list
    current_pattern

    #conditions
    has_pattern
    has_length
    has_letter
    has_no_letter

    # actions
    reset
    update_state
    update_word_count
    guess
    start_game
    get_wordlist_from_source
    get_guess_letter
    


    # event
    already_a_game => "There is a game already in progress"
    is_question 
    is_corect
    is_not_corect

    

    # utility
    filter_&_update_word_list
    
    
    """

    # event
    # already_a_game => "There is a game already in progress"
    # is_question 
    # is_corect
    # is_not_corect
    # is a new game
    # is done



    def is_game_over(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_game_over()")
        text = self.get_last_bot_msg()
        
        if re.findall("GAME OVER!",text,re.I):
            print("is gameover")
            answer = re.findall(r"The correct answer is: (.+)",text,re.I)
            if answer:
                print(f"\n\n [{self.__class__}]{self.__class__.__name__}() answer game over",answer[0])
                if not WordList.objects.filter(_word=answer[0]).exists(): WordList.objects.create(_word=answer[0])
            self.reset()
            self.start_game()

    def is_done(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_done()")
        text = self.get_last_bot_msg()+'\n'
        text += self.get_last_bot_msg(index=-2)
        if re.findall("Well done",text,re.I):
            answer = re.findall(r"The solution is: (.+)",text,re.I)
            if answer:
                print(f"\n\n [{self.__class__}]{self.__class__.__name__}() answer in is_done",answer[0])
                if not WordList.objects.filter(_word=answer[0]).exists(): WordList.objects.create(_word=answer[0])
                
            print("\n\n is done")
            self.reset()

    def is_new_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_new_game()")
        text = self.get_last_bot_msg()
        
        if re.findall(f"New game! The word is",text,re.I):
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() new game")

            self.reset()
            self.update_word_count(text)
            self.filter_update_word_list(self.has_length())
            self.guess()

    def already_a_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().already_a_game()")
        text = self.get_last_bot_msg()
        if re.findall(f"There is a game already in progress",text,re.I):
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() already a game")
            self.update_state(text)
            self.filter_update_word_list(self.has_pattern(),self.has_length(),self.has_no_letter())
            self.guess()

    def is_question(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        text = self.get_last_bot_msg()
        if re.findall(f"The letter was correct",text,re.I):
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() is question")
            self.update_state(text)
            self.filter_update_word_list(self.has_pattern())
            self.guess()

    def is_correct(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_correct()")
        text = self.get_last_bot_msg()
        if re.findall(f"The letter was correct",text,re.I):
            print(f"\n\n [{self.__class__}]{self.__class__.__name__}() is correct")
            self.update_state(text)
            self.filter_update_word_list(self.has_pattern())
            self.guess()
    
    def is_not_correct(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_not_correct()")
        text = self.get_last_bot_msg()
        if not re.findall(f"The letter was correct",text,re.I):
            self.update_state(text)
            self.filter_update_word_list(self.has_no_letter())
            self.guess()


    # utility
    def filter_update_word_list(self,*args):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().filter_update_word_list()")
        for con in args:
            self.word_list = list(filter(con,self.word_list))
            # print("total word",len(self.word_list))

    def wait_and_get_bot_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_bot_message()")
        for _ in range(20):
            if self.is_bot():return ''
            sleep(0.5)
        self.start_game()

    

    
        



    # actions
    # reset
    # update_state
    # update_word_count
    # guess
    # start_game
    # get_wordlist_from_source
    # get_guess_letter
    def reset(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().reset()")
        self.word_list = list()
        self.incorrect_letters = list()
        self.old_incorrect_letters = list()
        self.current_pattern=str()
        self.word_count = 0
        self.live = 0
        self.starter_letters = [
            'e','t','a','o','i','n','s','h',
            'r','d','l','u','c','m','f','w','y',
            'p','v','b','g','k','q','j','x','z'
        ]
        self.get_wordlist_from_source()

    def update_state(self,text):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().update_state()")
        incorrect_letters = re.findall(r"Incorrect letters: {(.+)}",text,re.I)
        if incorrect_letters:
            self.incorrect_letters = incorrect_letters[0].split(',')
            set_difference = set(self.starter_letters) - set(self.incorrect_letters)
            self.starter_letters = list(set_difference)
            # self.starter_letters = list(filter(lambda x:  x not in self.incorrect_letters and x not in [l.lower() for l in re.findall(r'([a-z])',self.current_pattern,re.I)],self.starter_letters))
            # print('incorrect letters',self.incorrect_letters)
            # print('starter letters',self.starter_letters)
            


        # current_pattern=str()
        current_pattern = re.findall(r"The word is: (.*)",text,re.I)
        if current_pattern:
            self.current_pattern = current_pattern[0]
            # print("pattern",self.current_pattern)

        # update word count
        self.update_word_count(text)

        # live
        live = re.findall(r"have (\d+) lives",text,re.I)
        if live:
            self.live = live[0]
            # print("live",self.live)

    def restart(self,*args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().restart()")
        self.driver.refresh()
        self.reset()
        self.start_game()

    def update_word_count(self,text):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().update_word_count()")
        word_count = re.findall(r"The word is:[ \n]+(.*)",text,re.I)
        if word_count:
            self.word_count = len(word_count[0].replace(' ',''))
            # print("word_count",self.word_count)


    def guess(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().guess()")
        self.tracker.reset()
        if self.starter_letters and not (len(self.word_list)>0 and len(self.word_list) < 40):
            self.send_msg(self.starter_letters.pop(0))
        else:
            letter = self.get_guess_letter()
            if letter:
                # print("letter found from choice")
                self.send_msg(choice(letter))
            else:
                # print("no choice")
                self.reset()
                self.filter_update_word_list(self.has_length())
        self.wait_and_get_bot_message()
            

    def start_game(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start_game()")
        try:
            self.check_autoplay('!h autoplay',"Hangman")
            for _ in range(10):
                self.driver.implicitly_wait(10)
                self.send_msg('!h')
                self.wait_and_get_bot_message()
                break
        except:
            pass

    def get_wordlist_from_source(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_wordlist_from_source()")
        if config['Hangman']['from_db']=='yes':
            self.word_list = [x.word for x in WordList.objects.all()]
        else:
            with open('word_list.json') as f:
                self.word_list = list(json.load(f))
            

    def get_guess_letter(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_guess_letter()")
        letter_from_pattern = re.findall(r'([a-zA-Z])',self.current_pattern,re.I)
        return list(filter(lambda x:x not in letter_from_pattern,set(''.join([x[0] for x in self.word_list]))))
    

    # conditions
    # has_parttern
    # has_length
    # has_letter
    # has_no_letter
    def has_pattern(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().has_pattern()")
        pattern = self.current_pattern.replace(' ','').replace('_','.')
        return lambda word:bool(re.findall(pattern,word[0],re.I))

    def has_length(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().has_length()")
        return lambda word:word[1]==self.word_count

    def has_letter(self,letter):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().has_letter()")
        return lambda word:letter in word[0]
        

    def has_no_letter(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().has_no_letter()")
        set_difference = set(self.incorrect_letters) - set(self.old_incorrect_letters)
        list_difference = list(set_difference)
        self.old_incorrect_letters = list(self.incorrect_letters)
        return lambda word:all([x.strip() not in word[0] for x in list_difference])


    
def main():
    username_1 = "Komp@gmail.com"
    password_1 = "123456"
    room_link = 'https://wolf.live/g/18900545'
    hm = Hangman(username_1,password_1,room_link=room_link)
    hm.tracker.wait(seconds=1)
    hm.start_game()
    hm.tracker.start()
    while not hm.is_stop():
        try:
            hm.is_new_game()
            hm.already_a_game()
            hm.is_question()
            hm.is_correct()
            hm.is_not_correct()
            hm.is_done()
            hm.is_game_over()
        except KeyboardInterrupt:
            hm.close()
            raise KeyboardInterrupt('stop by keyboard command')
        except StopBotError:
            hm.close()
            raise StopBotError('stop by bot command')
        except Exception as e:
            print("\n\n error\n",e)
            hm.driver.refresh()
            hm.start_game()
            hm.tracker.reset()
    hm.close()
    


    
    
# %%
if __name__ == "__main__":
    main()
    
    








# %%
