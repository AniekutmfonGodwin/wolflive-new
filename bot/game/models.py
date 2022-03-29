from django.db import models

# Create your models here.

class Gap(models.Model):
    question = models.CharField(db_index=True,max_length=200,default='')
    answer = models.CharField(max_length=100,default='')
    guess = models.CharField(default='',max_length=50)
    category = models.CharField(db_index=True,default='',max_length=50)

    def __str__(self):
        return f"==\nquestion: {self.question}\nanswer: {self.answer}\ncategory: {self.category}\n=="



class Quiz(models.Model):
    question = models.CharField(db_index=True,max_length=200,default='')
    answer = models.CharField(max_length=100,default='')
    optiona = models.CharField(max_length=100,default='')
    optionb = models.CharField(max_length=100,default='')
    optionc = models.CharField(max_length=100,default='')
    optiond = models.CharField(max_length=100,default='')
    guess = models.CharField(max_length=100,default='')

    def __str__(self):
        return f"==\nquestion: {self.question}\nanswer: {self.answer}\n=="




    
class GuessWhat(models.Model):
    image_code = models.CharField(db_index=True,max_length=50,default='')
    image_url = models.URLField(max_length=200,null=True,blank=True)
    answer = models.CharField(max_length=50,default='')
    guess = models.CharField(default='',max_length=50)
    category = models.CharField(db_index=True,default='',max_length=50)

    def __str__(self):
        return f"==\nimage_code: {self.image_code}\nanswer: {self.answer}\ncategory: {self.category}\n=="





