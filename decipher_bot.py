# %%
from dataclasses import dataclass,field
from strategies.exceptions import StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from time import sleep
from bs4 import BeautifulSoup
import configparser
config = configparser.ConfigParser()
config.read('config.ini')



# %%
@dataclass
class Deciper_Bot(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str = field(default_factory=lambda:'https://wolf.live/g/18336134')
    stop_agent:bool = field(default_factory=lambda:False)


    def __post_init__(self):
        self.login()

    

    # utility

    


    def restart(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().restart()")
        self.close()
        self.login()
        self.send_msg("!decipher next")

    
    def wait_and_get_user_message(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().wait_and_get_user_message()")
        for _ in range(50):
            if self.is_bot() or self.is_stop():return ''
            self.tracker.wait(0.5)

    

    def get_answer(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        is_question = False
        if self.get_latest_bot_msgs()[-1].get_attribute('render-tag')=="palringo-chat-message-pack":
            elem = self.qs.action(".shadowRoot").getOneShadowRoot("palringo-chat-message-pack").getOne("iframe").execute(self.get_latest_bot_msgs()[-1])
            self.driver.switch_to.frame(elem)
            content = self.driver.page_source
            self.driver.switch_to.default_content()
            soup = BeautifulSoup(content, 'html.parser')
            self.tracker.reset()
            if soup.select_one('.decipher-default'):
                code = dict([x.text.split(' = ') for x in soup.select('.decipher-default__content__middle__table__text-bubble__text')])
                decipher_word = list(soup.select_one('.decipher-default__content__footer__word').text)
                answer = ''.join([code[x] for x in decipher_word])
                print("answer =",answer,'\n')
                self.send_msg(answer)
                self.wait_and_get_user_message()
                is_question = True
            return is_question
            

    def on_success(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().on_success()")
        text = self.get_last_bot_msg()
        if "That's it!" in text:
            print("you win")
            if 'off' in config['Decipher']['autoplay'].lower():
                self.send_msg('!decipher next')
            

    # actions
    def start(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().start()\n")
        self.check_autoplay('!decipher autoplay','decipher')
        self.tracker.wait(6)
        for _ in range(5):
            try:
                self.send_msg("!decipher")
                break
            except:
                pass




def main():
    username_1 = "Komp@gmail.com"
    password_1 = "123456"
    room_link = 'https://wolf.live/g/18900545'
    d = Deciper_Bot(username_1,password_1,room_link)
    d.tracker.wait(4)
    if not d.get_answer():
        d.start()
    d.tracker.start(hours=2)
    while not d.is_stop():
        try:
            d.get_answer()
            d.on_success()
        except KeyboardInterrupt:
            raise KeyboardInterrupt("stop bot by keyboard command")
        except StopBotError:
            raise StopBotError("stop bot by bot command")
        except:
            d.tracker.wait(d.tracker.get_time)
        
        
        
        
    d.close()

    

# %%
if __name__ == "__main__":
    main()

