# %%
from dataclasses import dataclass,field
from strategies.main import BaseWolfliveStrategy, CheckStrategy, GetMessageStrategy, LoginStrategy, SendMessageStrategy
import json
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
# %%
@dataclass
class HunterHeroHeistFishing(
    BaseWolfliveStrategy,
    LoginStrategy,
    GetMessageStrategy,
    SendMessageStrategy,
    CheckStrategy
):
    username:str
    password:str
    room_link:str = field(default_factory=lambda:'https://wolf.live/g/18311932')

    def __post_init__(self):
        self.login()
        self.tracker.wait(2)
        self.main()
        self.tracker.start()

    def run_hunter(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().run_hunter()")
        commands = json.loads(config['Hunter']['commands'])
        if commands:
            try:
                for command in commands: 
                    data = command.split(':')
                    self.send_msg(f"!hunt {data[0]} {data[1]}")
                    self.tracker.wait(10)
            except:
                print("incorrect command")
        else:
            self.send_msg("!hunt")

    def restart(self):
        return self.main()

    def run_fishing(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().run_fishing()")
        commands = json.loads(config['Fishing']['commands'])
        if commands:
            try:
                for command in commands: 
                    data = command.split(':')
                    self.send_msg(f"!fish {data[0]} {data[1]}")
                    self.tracker.wait(10)
            except:
                print("incorrect command")
        else:
            self.send_msg(f"!fish")
            
        
            

    def run_hero(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().run_hero()")
        if config['HeroSquad']['count']:
            self.send_msg(f"!hero {config['HeroSquad']['count']}")
        else:
            self.send_msg("!hero")

    def run_heist(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().run_heist()")
        if config['Heist']['count']:
            self.send_msg(f"!heist {config['Heist']['count']}")
        else:
            self.send_msg("!heist")


    def main(self):
        print(f"\n\n [{self.__class__}]{self.__class__.__name__}().main()")
        self.tracker.start()
        while not self.is_stop():
            if config['Fishing']['play'].lower() =='yes':
                self.run_fishing() 
                self.tracker.wait(5)
            if config['Heist']['play'].lower() =='yes':
                self.run_heist()
                self.tracker.wait(5)
            if config['HeroSquad']['play'].lower() =='yes':
                self.run_hero()
                self.tracker.wait(5)
            if config['Hunter']['play'].lower() =='yes':
                self.run_hunter()
            self.tracker.wait(60)
            self.tracker.reset()
        

    

def main():
    username_1 = "Komp@gmail.com"
    password_1 = "123456"
    room_link = 'https://wolf.live/g/18900545'
    HunterHeroHeistFishing(username_1,password_1,room_link)
    



    
    
# %%
if __name__ == "__main__":
    main()
    

    
    
    
# %%


