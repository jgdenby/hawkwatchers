from django.urls import path
from django.conf.urls import url

from hawk_tracker import views

app_name = 'hawk_tracker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/statement/', views.StatementView.as_view(), name='statement'),
    path('{%/hawk_tracker/add_query/}', views.add_query, name='add_query'),
    path('{%/hawk_tracker/query/}', views.query, name='query'), # NEW MAPPING: fix
 ]

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^add_query/$', views.add_query, name='add_query'), # NEW MAPPING!
#     url(r'^query/(?P<query_name_url>\w+)$', views.query, name='query')
# ]
#     