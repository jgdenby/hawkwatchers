from django import forms
from .models import Query, Answer


class QueryForm(forms.ModelForm):
    #name = forms.CharField()
    text = forms.CharField(max_length=2500, help_text="Please enter a statement you would like Hawkwatchers to analyze",\
     widget=forms.Textarea(), initial="Add text here...")
   

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Query
        fields = ("query_text",) 

# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Page

#         # What fields do we want to include in our form?
#         # This way we don't need every field in the model present.
#         # Some fields may allow NULL values, so we may not want to include them...
#         # Here, we are hiding the foreign key.
#         fields = ('title', 'url', 'views')