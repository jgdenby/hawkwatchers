from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import QueryForm
from .models import Answer, Query, Statement

class IndexView(generic.ListView):
    template_name = 'hawk_tracker/index.html'
    context_object_name = 'latest_statement_list'

    def get_queryset(self):
        """Return the latest published statements."""
        return Statement.objects.order_by('-statement_last')[:5]

    # def get_queryset(self):
    #     """Return the latest published queries."""
    #     return Query.objects.order_by('-query_date')[:5]

class StatementView(generic.ListView):
    template_name = 'hawk_tracker/index.html'
    context_object_name = 'latest_statement_list'

    def get_statementset(self):
        """Return the latest published statements."""
        return Statement.objects.order_by('-statement_last')[:5]

class DetailView(generic.DetailView):
    model = Statement
    template_name = 'hawk_tracker/detail.html'


class ResultsView(generic.DetailView):
    model = Query
    template_name = 'hawk_tracker/results.html'

    # def get_results(self): # WE WANT TO LINK THIS TO OUR MODEL RESULTS
    #     """Return the last five published queries."""
    #     return Query.objects.order_by('-query_date')[:5]


def query(request, query_name_url):
    # Request our context from the request passed to us.
    #context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    query_name = query_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'query_name': query_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        query = Query.objects.get(name=query_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        query = Query.objects.filter(query=query)

        # Adds our results list to the template context under name pages.
        context_dict['query'] = query
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['query'] = query
    except Query.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('hawk_tracker/query.html', context_dict)

def add_query(request):
    # Get the context from the request.
    #context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = QueryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = QueryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('hawk_tracker/add_query.html', {'form': form})





# def index(request):
#     # Obtain the context from the HTTP request.
#     context = RequestContext(request)

#     # Query for categories - add the list to our context dictionary.
#     query_list = Query.objects.order_by('query_date')[:5]
#     context_dict = {'queries': query_list}

#     # The following two lines are new.
#     # We loop through each category returned, and create a URL attribute.
#     # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
#     for query in query_list:
#         query.url = query.name.replace(' ', '_')

#     # Render the response and return to the client.
#     return render_to_response('hawk_tracker/index.html', context_dict, context)
