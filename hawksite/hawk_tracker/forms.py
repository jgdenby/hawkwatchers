from django import forms
from .models import Query, Answer

NEURAL_NETWORKS = 'NN'
DECISION_TREE = 'DT'
BAGGING = 'BAG'
NAIVE_BAYES = 'NB'

MODEL_CHOICES = [ ('HELP','Choose A Prediction Model!' ),
    ('NN', 'Neural Networks'),
    ('DT', 'Decision Tree'),
    ('BAG', 'Bagging (Decision Tree)'),
    ('NB', 'Naive Bayes')]

class QueryForm(forms.ModelForm):
    query_text = forms.CharField(max_length=5000,
    widget = forms.Textarea(attrs={'cols': 110, 'rows': 20}), \
    initial="Add statement here...", label = '')
    query_method = forms.ChoiceField(widget=forms.Select(),
                              required=True, choices = MODEL_CHOICES,label = '')



    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Query
        fields = ("query_text", "query_method")
        
