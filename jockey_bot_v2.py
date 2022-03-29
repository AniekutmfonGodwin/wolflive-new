# %%
from dataclasses import dataclass
from typing import List, Optional
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
        print("\n\n restart()")
        self.main()

    def get_health(self):
        self.goto_private()
        self.send_message_private("!jockey view")

    
    def is_iframe(self, private=True, index=-1):
        print("\n\n is_iframe()")
        self.goto_private()
        elements: List[WebElement] = self.get_latest_bot_msgs(private=private)
        if elements and elements[index].get_attribute("render-tag"):
            return elements[index]

    def get_health(self, index=-1):
        print("\n\n get_health()")
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
        print("\n\n train_for_speed()")
        self.send_message_private("!سباق تدريب كل 100")

    def race(self):
        print("\n\n race()")
        self.send_msg("!س جلد")

    def is_health_notification(self):
        print("\n\n is_health_notification()")
        self.tracker.reset()
        self.goto_private()
        elements: List[WebElement] = self.get_latest_bot_msgs(private=True)
        if not elements: return
        element: WebElement = elements[-1]
        message_samples = ["عادت الطاقة الكاملة!","animal is back to full"]
        if element and element.get_attribute("render-tag") in "palringo-chat-message-text":
            return any([x in element.text for x in message_samples])
            

    def train_for_stamina(self):
        print("\n\n train_for_stamina()")
        self.send_message_private("!سباق تدريب كل 100")

    def train_for_agile(self):
        print("\n\n train_for_agile()")
        self.send_message_private("!سباق تدريب كل 100")

    def main(self):
        print("\n\n main()")
        self.tracker.wait(seconds=10)
        self.tracker.start()
        race = config["Jockey_v2"]["race"] or 1
        race = int(race)

        train = config["Jockey_v2"]["train"] or 80
        train = int(train)
        health = self.get_health()
        if not health:
            health = 99
        while True:
            # try:
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


# %%

if __name__ == "__main__":
    username_1 = "jeremy.trac@appzily.com"
    password_1 = "951753"
    j = Jockey_Bot_v2(username_1, password_1)
    j.main()
    try:
        j.driver.quit()
    except:
        pass

# %%

