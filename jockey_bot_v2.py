# %%
from dataclasses import dataclass
from typing import List, Optional
from strategies.exceptions import  StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


# %%
@dataclass
class Jockey_Bot_v2(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    
    username:str
    password:str
    private_url:Optional[str] ='https://wolf.live/u/80277459'
    room_link:Optional[str] = 'https://wolf.live/g/18900545'

    def __post_init__(self):
        self.login()
    

    def restart(self, *args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().restart()")
        self.login()
        self.main()

    # def get_health(self):
    #     self.goto_private()
    #     self.send_message_private("!jockey view")

    
    def is_iframe(self, private=True, index=-1):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_iframe()")
        self.goto_private()
        elements: List[WebElement] = self.get_latest_bot_msgs(private=private)
        if elements and elements[index].get_attribute("render-tag"):
            return elements[index]

    def get_health(self, index=-1):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().get_health()")
        self.send_message_private("!jockey view")
        self.tracker.wait(seconds=3)

        for _ in range(5):
            try:
                iframe_element = self.is_iframe(index=index)
                if iframe_element:
                    iframe = self.qs.action(".shadowRoot").getOneShadowRoot(
                        "palringo-chat-message-pack",
                    ).getOne("iframe").execute(iframe_element)
                    self.driver.switch_to.frame(iframe)
                    percentage: str = self.driver.find_element(By.CSS_SELECTOR,
                                                               ".jockey-mp-view__content__energyPercentage").text or ''
                    percentage = percentage.replace("%", '')
                    percentage = float(percentage)
                    return percentage
                raise Exception("iframe element does not exist")
            except:
                self.driver.refresh()
                self.tracker.wait(seconds=10)

    

    def train_for_speed(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_speed()")
        self.send_message_private("!سباق تدريب كل 100")

    def race(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().race()")
        self.send_msg("!س جلد")

    def is_health_notification(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().is_health_notification()")
        self.tracker.reset()
        self.goto_private()
        elements: List[WebElement] = self.get_latest_bot_msgs(private=True)
        if not elements: return
        element: WebElement = elements[-1]
        message_samples = ["عادت الطاقة الكاملة!","animal is back to full"]
        if element and element.get_attribute("render-tag") in "palringo-chat-message-text":
            return any([x in element.text for x in message_samples])
            

    def train_for_stamina(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_stamina()")
        self.send_message_private("!سباق تدريب كل 100")

    def train_for_agile(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_agile()")
        self.send_message_private("!سباق تدريب كل 100")

    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        self.tracker.start(hours=10)
        self.tracker.wait(seconds=10)
        race = config["Jockey_v2"]["race"] or 1
        race = int(race)

        train = config["Jockey_v2"]["train"] or 80
        train = int(train)
        health = self.get_health()
        if not health:
            health = 99
        while True:
            try:
                if not (health >= 100):
                    self.goto_private()
                    self.tracker.wait_til_condition(
                        conditions=[
                            self.is_health_notification
                        ],
                        delay_in_seconds=5
                    )
                health = 0

                for _ in range(race):
                    self.send_msg("!jockey race")
                    self.tracker.wait(seconds=60)

                self.send_message_private("!jockey train all " + str(train))
                self.tracker.wait(seconds=10)
                self.tracker.reset()
                
            except KeyboardInterrupt:
                raise KeyboardInterrupt("stop bot by keyboard interrupt")
            except StopBotError:
                raise StopBotError("stop bot by stop but command")
            except Exception:
                self.tracker.wait(self.tracker.get_time)

def main():
    # username = "jeremy.trac@appzily.com"
    # password = "951753"
    username = "Komp@gmail.com"
    password = "123456"
    j = Jockey_Bot_v2(username, password)
    j.main()
    try:
        j.driver.quit()
    except:
        pass

# %%

if __name__ == "__main__":
    main()

# %%

