from django.urls import path 
from a_user.views import *

urlpatterns = [
    path('',profile_view,name='profile'),
    path('edit/',profile_edit_view,name='profile_edit')
]