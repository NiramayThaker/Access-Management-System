from django.shortcuts import render, HttpResponse, redirect
from .forms import RegisterForm, PostForms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Post
from django.contrib.auth.models import User, Group


# Create your views here.
@login_required(login_url="/login")
def index(request):
	posts = Post.objects.all()
	context = {"posts": posts}

	if request.method == 'POST':
		post_id = request.POST.get('post-id')
		user_id = request.POST.get('user-id')

		if post_id:
			post = Post.objects.filter(id=post_id).first()
			if post and (post.author == request.user or request.user.has_perms("main.delete_post")):
				post.delete()
		elif user_id:
			user = User.objects.get(id=user_id)
			if user and user.is_staff:
				try:
					group = Group.objects.get(name='default')
					group.user_set.remove(user)
				except:
					pass
				try:
					group = Group.objects.get(name='mod')
					group.user_set.remove(user)
				except:
					pass

			return redirect('/')

	return render(request, 'main/home.html', context=context)


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
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
	if request.method == "POST":
		form = PostForms(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()

			return redirect("/")
	else:
		form = PostForms()

	context = {"post_form": form}
	return render(request, "main/posts.html", context=context)
