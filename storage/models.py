from django.db import models

class WordList(models.Model):
    _word = models.CharField( max_length=1000)
  

    def __str__(self):
        return self._word

    @property
    def word(self):
        return [self._word,len(self._word)]


class GuessWhat(models.Model):
    image_code = models.CharField(db_index=True,max_length=50,default='')
    image_url = models.URLField(max_length=200,null=True,blank=True)
    answer = models.CharField(max_length=50,default='')
    guess = models.CharField(default='',max_length=50)
    category = models.CharField(db_index=True,default='',max_length=50)

    def __str__(self):
        return f"==\nimage_code: {self.image_code}\nanswer: {self.answer}\ncategory: {self.category}\n=="

class PuzzleModel(models.Model):

    scrammle_link = models.URLField( max_length=200)
    arranged_link = models.URLField( max_length=200)
    moves = models.CharField(max_length=50)


    

