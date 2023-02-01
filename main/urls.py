from django.urls import path
from . import views


urlpatterns = [
	path("", views.index, name='home'),
	path("home", views.index, name='home'),
	path("sign-up", views.sign_up, name='sign-up'),
	path("create-post", views.create_post, name='create-post'),
]
