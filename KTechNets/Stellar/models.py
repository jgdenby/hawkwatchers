from django.db import models


class ArtChoice(models.Model):
    """
    This is used to create a Query object whose text can be processed by the models
    as it has all the necessary attributes to run the model and create the display.
    """

    artchoice_name = models.CharField(max_length=1200)
    artchoice_method = models.CharField(max_length=1200, default="Sim")
    artchoice_size = models.IntegerField(default=10)
    artchoice_answer = models.CharField(max_length=1200, null=True)

    def __str__(self):
        return artchoice_answer


class ArtPath(models.Model):
    """
    This is used to create an Answer object that will be linked to a Query object.
    """

    query_answer = models.OneToOneField(
        ArtChoice,
        on_delete=models.CASCADE,
        primary_key=True,
    )  # an answer for a query
    artpath_text = models.CharField(max_length=200)  # hawkish, dovish
    artpath_num = models.CharField(
        max_length=20
    )  # boolean associated to the nltk model

    def __str__(self):
        return self.artpath_text
