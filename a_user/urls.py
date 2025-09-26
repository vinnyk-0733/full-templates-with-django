from django.urls import path 
from a_user.views import *

urlpatterns = [
    path('',profile_view,name='profile'),
    path('edit/',profile_edit_view,name='profile_edit'),
    path('onboarding/',profile_edit_view,name = 'profile_onboarding'),
    path('setting/',profile_setting_view,name = 'profile_setting'),
    path('emailchange/',profile_emailchange,name='profile_emailchange'),
    path('emailverify/',profile_emailverify,name= 'profile_emailverify'),
    path('delete/',profile_delete_view,name='profile_delete'),

]