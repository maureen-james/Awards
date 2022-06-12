from . import views
from django.urls import path



urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('search/', views.search_results, name='search_results'),
    path('user/<user_id>', views.profile, name='profile'),
    path('user/update/profile', views.update_profile, name='updateprofile'),
    path('projectdetails/<project_id>',views.project_details,name='projectdetails'),
    path('rates/<project_id>',views.submit_rates,name='submitrates'),
    
]