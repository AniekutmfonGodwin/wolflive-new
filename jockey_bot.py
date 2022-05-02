# %%
from dataclasses import dataclass, field
from typing import Optional
from strategies.exceptions import SignalRestartError, StopBotError
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
    test:bool = field(default_factory=bool)

    def __post_init__(self):
        self.login()
        
    
    def restart(self, *args, **kwargs):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().restart()")
        if not self.is_login:self.update_driver()
        self.main()
        

    def train_for_speed(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_speed()")
        self.send_message_private("!سباق تدريب كل 100")
        self.wait_for_bot_private()

    # utility
    def train(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train()")
        self.tracker.wait(seconds=10)
        while not self.is_stop():
            try:
                self.goto_private()
                self.train_for_agile()
                self.tracker.wait(seconds=60)
                self.train_for_speed()
                self.tracker.wait(seconds=60)
                self.train_for_stamina()
                self.tracker.wait(seconds = 60)
                print(f"\n\n [{self.__class__}]{self.__class__.__name__}() running")
            except KeyboardInterrupt:
                raise KeyboardInterrupt("stop bot by keyboard interrupt")

            except StopBotError:
                raise StopBotError("stop bot by bot interrupt")
            except SignalRestartError:
                self.close()
                raise SignalRestartError
            except Exception:
                self.tracker.wait(self.tracker.get_time)
            self.tracker.wait(60)  

    def race(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().race()")
        self.goto_group()
        while not self.is_stop():
            self.send_msg("!س جلد")
            self.wait_for_bot_group()
            self.tracker.wait(60)
            


    def train_for_stamina(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_stamina()")
        self.send_message_private("!سباق تدريب كل 100")
        self.wait_for_bot_private()
        
    def train_for_agile(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().train_for_agile()")
        self.send_message_private("!سباق تدريب كل 100")
        self.wait_for_bot_private()

    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")


def main():
    # username = "jeremy.trac@appzily.com"
    # password = "951753"
    username = "Komp@gmail.com"
    password = "123456"
    # action = sys.argv[1] if len(sys.argv) >1 else "train"

    for _ in range(20):
        try:
            j = Jockey_Bot(username,password)
            
            if 'race' in sys.argv:
                j.race()
                j.tracker.wait(seconds=10)
                print("\n\n  racing completed")
            else:
                j.train()
            j.close() 
            break
        except SignalRestartError:
            continue

def test():
    # username = "jeremy.trac@appzily.com"
    # password = "951753"
    username = "Komp@gmail.com"
    password = "123456"
    # action = sys.argv[1] if len(sys.argv) >1 else "train"

    for _ in range(20):
        try:
            return Jockey_Bot(username,password)
            
        except SignalRestartError:
            continue
        
    
# %%

if __name__ == "__main__" and "-i" not in sys.argv:
    main()
    
    
    
# %%

