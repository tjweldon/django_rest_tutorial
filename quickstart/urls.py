from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from quickstart import views

urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(), name=views.SnippetList.name),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name=views.SnippetDetail.name),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name=views.SnippetHighlight.name),
    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>/', views.UserDetail.as_view(), name=views.UserDetail.name),
]

urlpatterns = format_suffix_patterns(urlpatterns)
