from django.urls import path,include
from roboproject.views import PostAPI, post_comment, react, verify,get_unverified,get_projects
from rest_framework import routers


urlpatterns = [
    path('', PostAPI.as_view()),
    path('get_project/',get_projects, name= "projects_api"),
    path('<int:pk>/post_comment/',post_comment, name= "comment_api"),
    path('<int:pk>/<arg>/', react, name= "react_api"),
    path('<int:pk>/verify/', verify, name= "verify_api"),
    path('unverified_projects/', get_unverified, name= "admin_get_api"),
]