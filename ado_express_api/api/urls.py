from django.urls import path
from . import search_views

'''
/run/via-query
/run/via_latest
/run/via_numbers

/search/query
/search/via_latest
/search/via_numbers
'''

urlpatterns = [
    path('search/via-latest', search_views.search_via_latest_release),
    path('search/via-number', search_views.search_via_release_number),
    path('search/via-query', search_views.search_via_query)
]