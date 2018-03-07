from django.urls import path
from hawk_tracker import views

app_name = 'hawk_tracker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>', views.ResultsView.as_view(), name='result'),
    path('<int:pk>/statement/', views.StatementView.as_view(), name='statement'),
    path('add_query/', views.add_query, name='addquery'),
    path('about/', views.about, name='about'),
    path('add_query/result/', views.result, name='result'),
    
 ]

