# %%
from dataclasses import dataclass,field
from strategies.exceptions import SignalRestartError, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from bs4 import BeautifulSoup
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
import sys


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
    test:bool = field(default_factory=bool)


    def __post_init__(self):
        self.login()
        self.autoplay = config['Decipher']['autoplay'].lower().strip() in ["on","1",1]
        self.set_autoplay("!decipher autoplay")
        if not self.test:self.restart()

    

    # utility

    


    def restart(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().restart()")
        self.main()

    

    def get_answer(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_answer()")
        is_question = False
        if self.get_latest_bot_msgs()[-1].get_attribute('render-tag')=="palringo-chat-message-pack":
            elem = self.qs.action(".shadowRoot").getOneShadowRoot("palringo-chat-message-pack").getOne("iframe").execute(self.get_latest_bot_msgs()[-1])
            self.driver.switch_to.frame(elem)
            content = self.driver.page_source
            self.driver.switch_to.default_content()
            soup = BeautifulSoup(content, 'html.parser')
            if soup.select_one('.decipher-default'):
                code = dict([x.text.split(' = ') for x in soup.select('.decipher-default__content__middle__table__text-bubble__text')])
                decipher_word = list(soup.select_one('.decipher-default__content__footer__word').text)
                answer = ''.join([code[x] for x in decipher_word])
                print("answer =",answer,'\n')
                self.send_msg(answer)
                self.wait_for_bot_group()
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
        self.tracker.wait(6)
        for _ in range(5):
            try:
                self.send_msg("!decipher")
                break
            except:
                pass

    def main(self):
        self.tracker.wait(4)
        if not self.get_answer():
            self.start()
        
        while not self.is_stop():
            try:
                self.get_answer()
                self.on_success()
            except KeyboardInterrupt:
                raise KeyboardInterrupt("stop bot by keyboard command")
            except StopBotError:
                raise StopBotError("stop bot by bot command")
            except SignalRestartError:
                raise SignalRestartError
            except Exception as e:
                print(e)
                self.close()
                raise Exception
            




def main():
    username_1 = "Komp@gmail.com"
    password_1 = "123456"
    room_link = 'https://wolf.live/g/18900545'
    d:Deciper_Bot
    for _ in range(20):
        try:
            d = Deciper_Bot(username_1,password_1,room_link)
            break
        except KeyboardInterrupt:
            raise KeyboardInterrupt("stop bot by keyboard command")
        except StopBotError:
            raise StopBotError("stop bot by bot command")
        except SignalRestartError:
            continue
    if d:d.close()
    

def test():
    username_1 = "Komp@gmail.com"
    password_1 = "123456"
    room_link = 'https://wolf.live/g/18900545'
    d:Deciper_Bot
    for _ in range(20):
        try:
            return Deciper_Bot(username_1,password_1,room_link,test=True)
        except KeyboardInterrupt:
            raise KeyboardInterrupt("stop bot by keyboard command")
        except StopBotError:
            raise StopBotError("stop bot by bot command")
        except SignalRestartError:
            continue
        
    if d:d.close()

# %%
if __name__ == "__main__" and "-i" not in sys.argv:
    main()

