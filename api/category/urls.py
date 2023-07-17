from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.categories_list),
    path('get/<int:id>/', views.get_category_information),
    path('update/<int:id>/', views.update_category_information),
    path('create/', views.create_category_information),
    path('delete/<int:id>/', views.delete_category_information),
]
