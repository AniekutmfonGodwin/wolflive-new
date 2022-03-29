# %%
from dataclasses import dataclass,field
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
        self.tracker.start()

    

    # utility

    


    def restart(self):
        self.driver.refresh()
        self.send_msg("!decipher next")

    
    def wait_and_get_user_message(self):
        for _ in range(50):
            if self.is_bot() or self.is_stop():return ''
            self.tracker.wait(0.5)

    

    def get_answer(self):
        print("get_answer()")
        if self.get_latest_bot_msgs()[-1].get_attribute('render-tag')=="palringo-chat-message-pack":
            try:
                elem = self.qs.action(".shadowRoot").getOneShadowRoot("palringo-chat-message-pack").getOne("iframe").execute(self.get_latest_bot_msgs()[-1])
                # elem = self.expand_shadow_element(
                #     self.expand_shadow_element(self.get_latest_bot_msgs()[-1])
                # .find_element_by_css_selector('palringo-chat-message-pack')
                # ).find_element_by_css_selector('iframe')
                self.driver.switch_to.frame(elem)
                content = self.driver.page_source
                self.driver.switch_to.default_content()
                soup = BeautifulSoup(content, 'html.parser')
                self.tracker.reset(30.0)
                if soup.select_one('.decipher-default'):
                    code = dict([x.text.split(' = ') for x in soup.select('.decipher-default__content__table__cell')])
                    decipher_word = list(soup.select_one('.decipher-default__content__ciphered__word__text').text)
                    answer = ''.join([code[x] for x in decipher_word])
                    print("answer =",answer,'\n')
                    self.send_msg(answer)
                    self.wait_and_get_user_message()
                
            except:
                pass

    def on_success(self):
        text = self.get_last_bot_msg()
        if "That's it!" in text:
            print("you win")
            if 'off' in config['Decipher']['autoplay'].lower():
                self.send_msg('!decipher next')
            

    # actions
    def start(self):
        self.check_autoplay('!decipher autoplay','decipher')
        for _ in range(5):
            try:
                print("start()\n")
                self.send_msg("!decipher")
                break
            except:
                pass

    

    

# %%
if __name__ == "__main__":
    username_1 = "Komp@gmail.com"
    password_1 = "123456"
    d = Deciper_Bot(username_1,password_1)
    sleep(2)
    d.start()
    while not d.is_stop():
        try:
            d.get_answer()
            d.on_success()
        except:
            pass
        
        
    d.close()

# %%
# d.check_autoplay()
# %%
