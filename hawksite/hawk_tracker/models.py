
from django.db import models
from django.utils import timezone


class Query(models.Model):
    #query_title = models.CharField(max_length=1200)
    query_text = models.CharField(max_length=1200)
    query_date = models.DateTimeField(default=timezone.now, blank=True)
    query_method = models.CharField(max_length=1200, default = 'NN')
    query_answer = models.CharField(max_length=1200, default = 'NEUTRAL')


    def __str__(self):
        return self.query_text

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.query_date <= now


class Answer(models.Model):
    query_answer = models.OneToOneField(Query, on_delete=models.CASCADE, primary_key=True,) # an answer for a query
    #statement = models.ForeignKey(Query, on_delete=models.CASCADE) # an answer for a statement
    answer_text = models.CharField(max_length=200) # hawkish, dovish
    answer_num = models.IntegerField(default=0) #boolean associated to the nltk model

    def __str__(self):
        return self.answer_num

    #missing: answer --> link instance to the nltk model output
class Statement(models.Model):
    statement_title = models.CharField(max_length=1200, default ="Or find out what Hawkwatchers thinks about the latest Fed Statement!")
    statement_header = models.CharField(max_length=1200)
    statement_text = models.CharField(max_length=3200)
    statement_last = models.DateTimeField('date published')
    statement_next = models.CharField(max_length=1200, default ="Next Fed Interest Rate Decision: March 21, 2018")

    def __str__(self):
        return self.statement_text


