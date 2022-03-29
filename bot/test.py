import csv
import os
from main import *
from time import time


# t1 = time()
# with open('../anies/solve_guess_what.csv','r',newline='\n',encoding='utf-8') as file:
#     reader = [x for x in list(csv.DictReader(file,delimiter='|',quotechar='|')) if x['answer'] not in ['none','None',None]]
#     # print(reader[:20])
#     for data in reader:
#         if not GuessWhat.objects.filter(image_code=data.get("image_code")).exists():
#             GuessWhat.objects.create(image_code=data.get("image_code"),answer=data.get("answer"),image_url=data.get("image_url"),category='music')
#             # print(data)



# print("took ",time()-t1," sec")
# stop = None
# while not stop:
#     for x in range(1000000):
#         if x == 10:stop=True
#         if x == 10:break


gp = Gap.objects.create(question="test",answer="test",guess="test")

print(gp.guess)

