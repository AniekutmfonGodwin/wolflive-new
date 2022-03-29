# %%
# from jockey_bot import Jockey_Bot
from jockey_bot_v2 import Jockey_Bot_v2


# %%
username_1 = "jeremy.trac@appzily.com"
password_1 = "951753"
self = Jockey_Bot_v2(username_1,password_1)
# %%
self.login()

# %%
self.main()


# %%
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# %%
self.tracker.wait(seconds=10)
self.tracker.start()
race = config["Jockey_v2"]["race"] or 1
race = int(race)

train = config["Jockey_v2"]["train"] or 80
train = int(train)
health = self.get_health()
if not health:
    health = 99
# %%
self.send_message_private("!jockey view")
# %%
self.goto_private()
# %%
elements = self.get_latest_bot_msgs(private=True)
# %%
