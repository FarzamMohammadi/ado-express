from django.urls import path

from . import deploy_views, search_views

urlpatterns = [
    path('deploy', deploy_views.deploy),

    path('search/via-environment', search_views.search_via_release_environment),
    path('search/via-latest', search_views.search_via_latest_release),
    path('search/via-number', search_views.search_via_release_number),
    path('search/via-query', search_views.search_via_query),
]