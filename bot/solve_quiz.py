from dataclasses import dataclass
import re
import random
from time import sleep
from main import *
import main
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy


@dataclass
class SolveQuiz(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str
    private_url:str

    def __post_init__(self):
        self.login()
        
        # self.browser = browser
        # self.browser.driver.switch_to.window(self.browser.driver.window_handles[0])
        
        for _ in range(int(input("how many time do you want me to play the game \ne.g 10\n"))):
            try:
                self.main()
            except Exception as e:
                print("error occurred\n",e)
                continue


    def wait_for_bot_message_private(self):
        for _ in range(10):
            if self.is_bot_message_private():
                return self.get_last_message_private()
        return False

    def wait_for_bot_message_grp(self):
        for _ in range(10):
            if self.is_bot_message_grp():
                return self.get_last_msg()
        return False
            


    def is_bot_message_grp(self):
        return bool(re.search(r'bot',self.get_last_msg(),re.I))

    def is_correct(self,text=''):
        return bool(re.search(r'Correct you',text,re.I))

    def is_gameover(self,text=''):
        return bool(re.search(r'Incorrect answer - Game over',text,re.I))

    def bot_send_private_message(self,text=''):
        return bool(re.search(r'Thanks, you have a PM from me with your first question',text,re.I))

    def get_question_type(self,text=''):
        return 'unknown'

    def is_bot_message_private(self):
        return bool(re.search(r'bot',self.get_last_message_private(),re.I))


    

    def is_timeup(self,text=''):
        return bool(re.search(r'Times up',text,re.I))
        





    def get_answer(self,question,choice):
        if main.Quiz.objects.filter(question=question.get('question')).exists():
            data = main.Quiz.objects.get(question=question.get('question'))
            if data.answer:
                option = [x for x in list(question)[2:6] if data.answer in question[x]]
                if option:
                    answer = re.findall(r'option(a|b|c|d)',option[0],re.I)
                    if answer:
                        print("option from database",answer[0])
                        return answer[0]
        else:
            return choice
        return choice

    def is_question(self,text=''):
        return bool(re.findall(r'Type "E" to skip this question',text))
        
        

   

    def already_have_a_game(self,text=''):
        return bool(re.findall(r'You already have a game in progress',str(text),re.I))


    def get_question_and_options(self,text=''):
        question = r'\d\. (.+\??)'
        optiona = r'a\. (.+)\n?'
        optionb = r'b\. (.+)\n?'
        optionc = r'c\. (.+)\n?'
        optiond = r'd\. (.+)\n?'
        pattern = lambda x:re.findall(x,text,re.I)[0]
        
        return {'question':pattern(question),'answer':'None','optiona':pattern(optiona),'optionb':pattern(optionb),'optionc':pattern(optionc),'optiond':pattern(optiond),'question_type':self.get_question_type(text)}




    def main(self):
        for _ in range(100):
            self.goto_group()
            for _ in range(10):
                try:
                    self.send_msg('!quiz private')
                    break
                except:
                    sleep(2)
                    continue

            text = str(self.wait_for_bot_message_grp())
            assert type(text) == str,'bot message in group is not string'
            if self.already_have_a_game(text) or self.bot_send_private_message(text):
                self.goto_private()
                for _ in range(10):
                    text_private = str(self.wait_for_bot_message_private())
                    assert type(text_private) == str,'bot private message is not string'
                    # print("question",text_private)
                    # print(self.is_question(text_private))
                    if self.is_question(text_private):
                        
                        question = self.get_question_and_options(text_private)
                        

                        choice = random.choice(['a','b','c','d'])
                        if not main.Quiz.objects.filter(question=question.get('question')).exists():
                            main.Quiz.objects.create(question=question.get("question"),optiona=question.get("optiona"),optionb=question.get("optionb"),optionc=question.get("optionc"),optiond=question.get("optiond"),guess=choice)
                        answer = self.get_answer(question,choice)
                        # print(answer)
                        self.send_message_private(answer)
                        # self.send_message_private(choice) # this is for test remove in production
                        response = str(self.wait_for_bot_message_private())
                        if self.is_correct(str(response)):
                            print("you got the correct answer")
                            question['answer'] = question.get(f'option{choice}')
                            # print("quetion",question)
                            # self.add(**question)
                            if main.Quiz.objects.filter(question=question.get("question"),answer='').exists():
                                qz = main.Quiz.objects.get(question=question.get("question"))
                                qz.answer = answer=question.get("answer")
                                qz.save()
                            
                            
                        if self.is_gameover(response) or self.is_timeup(response):break
            #                 # goto start



def main():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    private_url = 'https://wolf.live/u/72810009'
    

    browser:SolveQuiz = None
    
    is_login = False
    
    for _ in range(5):
        try:
            browser = SolveQuiz(username_1, password_1,room_link,private_url)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        # except:
        #     print("no internet conenction,re-trying...")
        #     continue
    
    
    if browser:browser.close()


if __name__ == '__main__':
    main()