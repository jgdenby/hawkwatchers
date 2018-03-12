from django import forms
from .models import Query, Answer

MODEL_CHOICES = [ ('NO MODEL','Choose A Prediction Model!' ),
    ('NN', 'Neural Networks'),
    ('DT', 'Decision Tree'),
    ('BAG', 'Bagging (Decision Tree)'),
    ('NB', 'Naive Bayes')]

class QueryForm(forms.ModelForm):
    '''
    Creates a form object that will be rendered to the user in order 
    to submit a query to our model. 
    '''
    query_text = forms.CharField(max_length=5000,
    widget = forms.Textarea(attrs={'cols': 110, 'rows': 20}), \
    initial="Add statement here...", label = '')
    query_method = forms.ChoiceField(widget=forms.Select(),
                              required=True, choices = MODEL_CHOICES,label = '')

    # The models.py class that will be associated with this form. 
    
    class Meta:
        model = Query
        fields = ("query_text", "query_method")
        
