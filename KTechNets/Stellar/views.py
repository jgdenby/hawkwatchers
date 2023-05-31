from django.shortcuts import render
from django.shortcuts import render
from django.views import generic
from .forms import QueryForm
from .models import ArtChoice, ArtPath
from Stellar import stellar

# import enchant


class IndexView(generic.ListView):
    # Creates a view object associated with the index page of the website.
    template_name = "Stellar/index.html"
    context_object_name = "latest_statement_list"

    def get_queryset(self):
        """Return the latest published statements."""
        return ArtChoice.objects.order_by("-artchoice_name")[:5]


def about(request):

    # Redirect the user to the 'About' page of the website.
    return render(request, "Stellar/about.html")


def add_query(request):
    # Instantiate a new form object that allows the user to submit a query.
    form = QueryForm()

    # Render the form with error messages (if any).
    return render(request, "Stellar/add_query.html", context={"form": form})


def result(request):
    """
    Extracts the string associated with a users query to process it so
    that it can be taken as an input to our model.
    """
    if request.method == "POST":
        form = QueryForm(request.POST)  # Instantiate Query with user's input (text)

        text = form.data["artchoice_text"]
        method = form.data["artchoice_method"]
        size = form.data["artchoice_size"]
        if method == "NO MODEL":
            context = {"answer": "Seems you forgot to choose a  prediction model.. "}
        else:

            artchoice_answer = process_query(text, method, size)
            context = {
                "good": artchoice_answer[0],
                "answer": "\n".join(artchoice_answer[1][:10]),
                "tgnode": artchoice_answer[2],
                "plink": artchoice_answer[3],
            }

            query_inst = ArtChoice()
            query_inst.artchoice_answer = artchoice_answer[1]
            query_inst.artchoice_text = artchoice_answer[2]
            query_inst.artchoice_method = method
            query_inst.artchoice_size = size
            query_inst.save()
            ans_inst = ArtPath(
                query_answer=query_inst
            )  # Instantiate Answer object with the model result.
            ans_inst.text = artchoice_answer
            ans_inst.save()

    return render(request, "Stellar/add_query/result.html", context)
    # THE USER WILL BE REDIRECTED TO CHECK THE RESULT


def process_query(text, method, size):
    """
    Process a given query using the NLTK model

    Inputs:
        method: (str) the processing model selected
        query_answer: (str) the Query object returned to be passed
            to the NLTK model

    Output:
        msg: (str) based on the model's decision, words to be passed to the views page
    """

    res = stellar.get_playlist(text, method, size)

    return res
