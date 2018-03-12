from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import QueryForm
from .models import Answer, Query, Statement
from hawk_tracker import nn_model
import nltk
import enchant
from sklearn.model_selection import train_test_split

class IndexView(generic.ListView):
    # Creates a view object associated with the index page of the website. 
    template_name = 'hawk_tracker/index.html'
    context_object_name = 'latest_statement_list'

    def get_queryset(self):
        """Return the latest published statements."""
        return Statement.objects.order_by('-statement_last')[:5]

class StatementView(generic.ListView):
    # Creates a view object associated to the Statement objects in models.py
    template_name = 'hawk_tracker/index.html'
    context_object_name = 'latest_statement_list'

    def get_statementset(self):
        """Return the latest published statements."""
        return Statement.objects.order_by('-statement_last')[:5]

class DetailView(generic.DetailView):
    # Creates a view object associated with a page displaying a particular
    # Federal Reserve press release and its' details. 
    model = Statement
    template_name = 'hawk_tracker/detail.html'


def about(request):

    # Redirect the user to the 'About' page of the website. 
    return render(request, 'hawk_tracker/about.html')

def add_query(request):
    # Instantiate a new form object that allows the user to submit a query. 
    form = QueryForm()
    
    # Render the form with error messages (if any).
    return render(request, 'hawk_tracker/add_query.html', context = {'form': form})

def result(request):
    '''
    Extracts the string associated with a users query to process it so 
    that it can be taken as an input to our model. 
    '''
    if request.method == 'POST':
        form = QueryForm(request.POST) # Instantiate Query with user's input (text)
        
        text = form.data['query_text']
        method = form.data['query_method']
        if method == "NO MODEL":
            context = {'answer': "Seems you forgot to choose a  prediction model.. "}
        else:

            if check(text):
                    query_answer = process_query(method, text)
                    context = {'answer': query_answer[0], 'next': query_answer[1]}

            else:
                query_answer = "Our models say . . . This doesn't quite look like a Fed statement!"
                context = {'answer': query_answer}
                            
            query_inst = Query()
            query_inst.query_answer = query_answer
            query_inst.query_text = text
            query_inst.query_method = method
            query_inst.save()
            ans_inst = Answer(query_answer = query_inst) # Instantiate Answer object with the model result.
            ans_inst.text = query_answer
            ans_inst.save()
            
    return render(request,'hawk_tracker/add_query/result.html', context) 
    #THE USER WILL BE REDIRECTED TO CHECK THE RESULT


def check(new_text, thresh = .25):
    '''
    Checks whether the text entered resembles a Federal Reserve statements
    by checking length, language, and key wording. 
    
    Inputs:
        new_text: (str) text entered by user
        thresh: (int) minimum percentage of words in text that must be in 
            designated language - American English. 
            
    Output:
        Returns True if valid and False if not a valid statement
    '''
    outcome = []
    outcome.append(len(new_text) > 200)

    d = enchant.Dict('en_US')
    denom = len(word_list)
    
    word_list = new_text.split(' ')
    non_en = 0

    for w in word_list:
        if w:
            if not d.check(w):
                non_en += 1

    outcome.append(non_en/denom <= thresh)

    if "econ" not in new_text:
        outcome.append(False)
    else:
        True

    if False in outcome:
        return False
    else:
        return True

def process_query(method, query_answer):
    '''
    Process a given query using the NLTK model
    
    Inputs:
        method: (str) the processing model selected
        query_answer: (str) the Query object returned to be passed
            to the NLTK model
            
    Output:
        msg: (str) based on the model's decision, words to be passed to the views page
    '''
    
    res = nn_model.predict(method, query_answer)
    
    if res == True:
        msg = "HAWKISH!", "UP"
    else:
        msg = "DOVISH!", "DOWN"
    
    return msg
    
