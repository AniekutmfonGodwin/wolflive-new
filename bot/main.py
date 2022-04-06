import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot.settings')
django.setup()

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0,os.path.join(BASE_DIR))

# logic goes below

from game.models import (
    Gap,
    Quiz,
    GuessWhat
)






if __name__ == '__main__':
    quiz_data = {'question':'how are you','answer':'you',"category":'Music'}
    
    # Quiz.objects.create(**quiz_data)
    # print(Quiz.objects.all())
    # print(GuessWhat.objects.filter(image_code='123456').exists())

