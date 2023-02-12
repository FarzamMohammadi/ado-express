from django.urls import path
from . import search_views

'''
/run/query
/run/via_latest
/run/via_numbers

/search/query
/search/via_latest
/search/via_numbers
'''

urlpatterns = [
    path('search/query', search_views.search_via_query)
]