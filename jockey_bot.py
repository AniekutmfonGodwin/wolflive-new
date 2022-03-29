# %%
from dataclasses import dataclass
from typing import Optional
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
        print("\n\n restart()")
        self.main()
        


    def train_for_speed(self):
        print("\n\n train_for_speed()")
        self.send_message_private("!سباق تدريب كل 100")

    # utility
    def train(self):
        print("\n\n train()")
        self.tracker.wait(seconds=10)
        while not self.is_stop():
            self.goto_private()
            self.train_for_agile()
            self.train_for_speed()
            self.tracker.wait(seconds=60)
            self.train_for_stamina()
            self.tracker.wait(seconds = 60)
            print("\n\n running")

    def race(self):
        print("\n\n race()")
        self.send_msg("!س جلد")
            


    def train_for_stamina(self):
        print("\n\n train_for_stamina()")
        self.send_message_private("!سباق تدريب كل 100")
        
    def train_for_agile(self):
        print("\n\n train_for_agile()")
        self.send_message_private("!سباق تدريب كل 100")

    def main(self):
        print("\n\n main()")
    
# %%

if __name__ == "__main__":
    username_1 = "jeremy.trac@appzily.com"
    password_1 = "951753"
    j = Jockey_Bot(username_1,password_1)
    action = sys.argv[1] if len(sys.argv) >1 else "train"
    
    if action == 'train':j.train()
    if action == 'race':
        j.race()
        j.tracker.wait(seconds=10)
        print("\n\n racing completed")
    j.close() 
    
    
    
# %%

