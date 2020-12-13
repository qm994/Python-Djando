from django.urls import path
from user import views

#https://docs.djangoproject.com/en/3.1/intro/tutorial03/#namespacing-url-names#
# this set the namespace of the url
app_name = 'user' # we can reversly retrive the url by using 'user:create'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]