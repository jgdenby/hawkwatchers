from django import forms
from .models import ArtChoice

MODEL_CHOICES = [
    ("IP", "Influence path"),
    ("Sim", "Similarity path"),
    ("Rand", "Random path"),
]


class QueryForm(forms.ModelForm):
    """
    Creates a form object that will be rendered to the user in order
    to submit a query to our model.
    """

    artchoice_text = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(attrs={"cols": 80, "rows": 6}),
        initial='[if not sure, just enter "IDK" and we\'ll pick a cool one for you]',
        label="",
    )
    artchoice_method = forms.ChoiceField(
        widget=forms.Select(), required=True, choices=MODEL_CHOICES, label="Path style?"
    )

    artchoice_size = forms.IntegerField(label="Path size?")

    # The models.py class that will be associated with this form.

    class Meta:
        model = ArtChoice
        fields = ("artchoice_text", "artchoice_method", "artchoice_size")
