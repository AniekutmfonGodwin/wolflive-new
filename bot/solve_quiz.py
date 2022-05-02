from dataclasses import dataclass, field
import re
import random
from main import *
import main as mymain
from strategies.exceptions import SignalRestartError, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
import sys

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
    loop_count:int = field(default_factory=int)
    test:bool = field(default_factory=bool)

    def __post_init__(self):
        self.login()
        self.tracker.wait(5)
        if not self.test:self.restart()
        

    def restart(self):
        self.loop_count = self.loop_count or int(input("how many time do you want me to play the game \ne.g 10\n") or 10)
        loop = int(self.loop_count)
        for _ in range(loop):
            self.loop_count -=1
            try:
                self.main()
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except Exception as e:
                print("error occurred\n",e)
                continue


    def is_bot_message_grp(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_bot_message_grp()")
        return bool(re.search(r'bot',self.get_last_element().text,re.I))

    def is_correct(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_correct()")
        return bool(re.search(r'Correct you',text,re.I))

    def is_gameover(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_gameover()")
        return bool(re.search(r'Incorrect answer - Game over',text,re.I))

    def bot_send_private_message(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().bot_send_private_message()")
        return bool(re.search(r'you have a private message from me with your first question',text,re.I))

    def get_question_type(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_question_type()")
        return 'unknown'

    def is_bot_message_private(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_bot_message_private()")
        return bool(re.search(r'bot',self.get_last_message_private(),re.I))


    

    def is_timeup(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_timeup()")
        return bool(re.search(r'Times up',text,re.I))
        





    def get_answer(self,question,choice):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        if mymain.Quiz.objects.filter(question=question.get('question')).exists():
            data = mymain.Quiz.objects.filter(question=question.get('question')).first()
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
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_question()")
        return bool(re.findall(r'Type "E" to skip this question',text))
        
        

   

    def already_have_a_game(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().already_have_a_game()")
        return bool(re.findall(r'You already have a game in progress',str(text),re.I))


    def get_question_and_options(self,text=''):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_question_and_options()")
        question = r'\d\. (.+\??)'
        optiona = r'a\. (.+)\n?'
        optionb = r'b\. (.+)\n?'
        optionc = r'c\. (.+)\n?'
        optiond = r'd\. (.+)\n?'
        pattern = lambda x:re.findall(x,text,re.I)[0]
        
        return {'question':pattern(question),'answer':'None','optiona':pattern(optiona),'optionb':pattern(optionb),'optionc':pattern(optionc),'optiond':pattern(optiond),'question_type':self.get_question_type(text)}




    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        for _ in range(100):
            self.goto_group()
            for _ in range(10):
                try:
                    self.send_msg('!quiz private')
                    self.wait_for_bot_group()
                    break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except StopBotError:
                    raise StopBotError
                except SignalRestartError:
                    self.close()
                    raise SignalRestartError
                except Exception as e:
                    print(f"\n\n error\n\n[{self.__class__}]{self.__class__.__name__}().main({e})")
                    self.tracker.wait(2)
                    continue

            text = str(self.wait_for_bot_group())
            assert type(text) == str,'bot message in group is not string'
            if self.already_have_a_game(text) or self.bot_send_private_message(text):
                self.goto_private()
                for _ in range(10):
                    text_private = str(self.wait_for_bot_private())
                    assert type(text_private) == str,'bot private message is not string'
                    
                    if self.is_question(text_private):
                        self.tracker.reset()
                        question = self.get_question_and_options(text_private)
                        

                        choice = random.choice(['a','b','c','d'])
                        if not mymain.Quiz.objects.filter(question=question.get('question')).exists():
                            mymain.Quiz.objects.create(question=question.get("question"),optiona=question.get("optiona"),optionb=question.get("optionb"),optionc=question.get("optionc"),optiond=question.get("optiond"),guess=choice)
                        answer = self.get_answer(question,choice)
                        # print(answer)
                        self.send_message_private(answer)
                        # self.send_message_private(choice) # this is for test remove in production
                        response = str(self.wait_for_bot_private())
                        if self.is_correct(str(response)):
                            print("you got the correct answer")
                            question['answer'] = question.get(f'option{choice}')
                            # print("quetion",question)
                            # self.add(**question)
                            if mymain.Quiz.objects.filter(question=question.get("question"),answer='').exists():
                                qz = mymain.Quiz.objects.get(question=question.get("question"))
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
    
    for _ in range(20):
        try:
            browser = SolveQuiz(username_1, password_1,room_link,private_url,loop_count=getattr(SolveQuiz,"loop_count",0))
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            SolveQuiz.loop_count = browser.loop_count
            continue
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    
    if browser:browser.close()



def test():
    username_1 = 'Komp@gmail.com'
    password_1 = '123456'
    room_link = 'https://wolf.live/g/18900545'
    private_url = 'https://wolf.live/u/72810009'
    

    browser:SolveQuiz = None
    
    is_login = False
    
    for _ in range(5):
        try:
            return SolveQuiz(username_1, password_1,room_link,private_url,test=True)
            
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except StopBotError:
            raise StopBotError
        except SignalRestartError:
            raise SignalRestartError
        except Exception as e:
            print("no internet conenction,re-trying...",e)
            continue
    
    
    if browser:browser.close()


if __name__ == '__main__' and "-i" not in sys.argv:
    main()