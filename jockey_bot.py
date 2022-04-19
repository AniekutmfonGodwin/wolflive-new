# %%
from dataclasses import dataclass
from typing import Optional
from strategies.exceptions import StopBot, StopBotError
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
import sys


# %%
@dataclass
class Jockey_Bot(
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
        self.main()
        


    def train_for_speed(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_speed()")
        self.send_message_private("!سباق تدريب كل 100")

    # utility
    def train(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train()")
        self.tracker.start(hours=2)
        self.tracker.wait(seconds=10)
        while not self.is_stop():
            try:
                self.goto_private()
                self.train_for_agile()
                self.train_for_speed()
                self.tracker.wait(seconds=60)
                self.train_for_stamina()
                self.tracker.wait(seconds = 60)
                print(f"\n\n [{self.__class__}]{self.__class__.__name__}() running")
                self.tracker.reset()
            except KeyboardInterrupt:
                raise KeyboardInterrupt("stop bot by keyboard interrupt")

            except StopBotError:
                raise StopBotError("stop bot by bot interrupt")
            except Exception:
                self.tracker.wait(self.tracker.get_time)
                

    def race(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().race()")
        self.send_msg("!س جلد")
            


    def train_for_stamina(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_stamina()")
        self.send_message_private("!سباق تدريب كل 100")
        
    def train_for_agile(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_agile()")
        self.send_message_private("!سباق تدريب كل 100")

    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")

def main():
    # username = "jeremy.trac@appzily.com"
    # password = "951753"
    username = "Komp@gmail.com"
    password = "123456"
    j = Jockey_Bot(username,password)
    action = sys.argv[1] if len(sys.argv) >1 else "train"
    
    if action == 'train':j.train()
    if action == 'race':
        j.race()
        j.tracker.wait(seconds=10)
        print("\n\n  racing completed")
    j.close() 
    
# %%

if __name__ == "__main__":
    main()
    
    
    
# %%

