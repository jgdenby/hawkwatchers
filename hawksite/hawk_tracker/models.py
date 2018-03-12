
from django.db import models
from django.utils import timezone

class Query(models.Model):
    '''
    This is used to create a Query object whose text can be processed by the models
    as it has all the necessary attributes to run the model and create the display.  
    '''
    query_text = models.CharField(max_length=1200)
    query_date = models.DateTimeField(default=timezone.now, blank=True)
    query_method = models.CharField(max_length=1200, default = 'NN')
    query_answer = models.CharField(max_length=1200, default = 'NEUTRAL')

    def __str__(self):
        return self.query_text

class Answer(models.Model):
    '''
    This is used to create an Answer object that will be linked to a Query object. 
    '''
    query_answer = models.OneToOneField(Query, on_delete=models.CASCADE, primary_key=True,) # an answer for a query
    answer_text = models.CharField(max_length=200) # hawkish, dovish
    answer_num = models.CharField(max_length=20) #boolean associated to the nltk model

    def __str__(self):
        return self.answer_text

class Statement(models.Model):
    '''
    Contains information related to a particular Federal Reserve press release. 
    The attributes are those which we want to display on the website.
    These are directly added by the administrator only, not by a user. 
    '''
    statement_title = models.CharField(max_length=1200, default ="Or find out what Hawkwatchers thinks about the latest Fed Statement!")
    statement_header = models.CharField(max_length=1200)
    statement_text = models.CharField(max_length=3200)
    statement_last = models.DateTimeField('date published')
    statement_next = models.CharField(max_length=1200, default ="Next Fed Interest Rate Decision: March 21, 2018")

    def __str__(self):
        return self.statement_text


