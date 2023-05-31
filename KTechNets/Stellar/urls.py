from django.urls import path
from Stellar import views

# Contains and generates the url paths for all pages in the website."

app_name = "Stellar"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("add_query/", views.add_query, name="addquery"),
    path("about/", views.about, name="about"),
    path("add_query/result/", views.result, name="result"),
]
