from . import views
from django.urls import path



urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('search/', views.search_results, name='search_results'),
    path('user/<user_id>', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/addproject/', views.add_project, name='add_project'),
    path('projectdetails/<project_id>',views.project_details,name='projectdetails'),
    path('profile/api/project/', views.ProjectList.as_view(),name=''),
    path('project/rate/<int:id>/', views.rate_project, name='rate_project'),
    path('profile/api/profile/', views.ProfileList.as_view(),name=''),
    # path('user/profile/', views.profile, name='profile'),
    # path('user/<user_id>', views.profile, name='profile'),
    # path('user/profile/<user_id>', views.update_profile, name='updateprofile'),
    # path('updateprofile', views.update_profile, name='updateprofile'),
    # path('rates/<project_id>',views.submit_rates,name='submitrates'),
]