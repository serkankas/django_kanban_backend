from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.user_list),
    path('get/<int:id>/', views.get_user_information),
    path('create/', views.create_user_information),
    path('update/<int:id>/', views.update_user_information),
    path('delete/<int:id>/', views.delete_user_information),
    path('change_password/<int:id>/', views.change_user_password),
]
