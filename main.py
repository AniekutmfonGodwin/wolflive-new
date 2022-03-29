import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newBot.settings')
django.setup()


# logic goes below

from storage.models import (
 WordList,
 GuessWhat
)






if __name__ == '__main__':
    word = {'_word':"name"}
    
    WordList.objects.create(**word)
    print(WordList.objects.all())

