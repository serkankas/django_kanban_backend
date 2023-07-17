from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.item_list),
    path('get/<int:id>/', views.get_item_information),
    path('update/<int:id>/', views.update_item_information),
    path('create/', views.create_item_information),
    path('delete/<int:id>/', views.delete_item_information),
]
