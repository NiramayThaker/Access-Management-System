from django.shortcuts import render, HttpResponse, redirect
from .forms import RegisterForm, PostForms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


# Create your views here.
@login_required(login_url="/login")
def index(request):
	return render(request, 'main/home.html')


def sign_up(request):
	# if we get post req we'll make new user Form
	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)

			return redirect('/home')

	# else we will render the empty form on the screen
	else:
		form = RegisterForm()

	context = {"form": form}
	return render(request, 'registration/sign_up.html', context=context)


@login_required(login_url="/login")
def create_post(request):
	post_form = PostForms()
	if request.method == "POST":
		post_form = PostForms(request.POST)
		if post_form.is_valid():
			post_form.save(commit=False)
			post_form.author = request.user
			post_form.save()

			return redirect("/")

	context = {"post_form": post_form}
	return render(request, "main/posts.html", context=context)
