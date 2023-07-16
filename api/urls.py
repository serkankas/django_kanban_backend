from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('user/', include('api.user.urls')),
    path('category/', include('api.category.urls')),
    path('board/', include('api.board.urls')),
]
