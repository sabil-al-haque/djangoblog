from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm,ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .models import Contact, Post
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
  posts = Post.objects.all()

  return render(request, 'blog/home.html',{'posts':posts})



def about(request):
    return render(request, 'blog/about.html')


def contact(request):
  if request.method == 'POST':
   form = ContactForm(request.POST)
   if form.is_valid():
    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    phone = form.cleaned_data['phone']
    comment = form.cleaned_data['comment']
    pst = Contact(name=name, email=email,phone=phone,comment=comment)
    pst.save()
    form = ContactForm()
  else:
   form = ContactForm() # ei form er jonnoi contact.html e 4 ta field dekha jay
  return render(request, 'blog/contact.html', {'form':form})
    




def dashboard(request):
    return render(request, 'blog/dashbord.html')






def signup(request):
 if request.method == "POST":
  form = SignUpForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! You have become an Author.')
   user = form.save()
   group = Group.objects.get(name='Author')
   user.groups.add(group)
 else:
  form = SignUpForm()
 return render(request, 'blog/signup.html', {'form':form})




def login(request):
 if not request.user.is_authenticated:
  if request.method == "POST":
   form = LoginForm(request=request, data=request.POST)
   if form.is_valid():
    uname = form.cleaned_data['username']
    upass = form.cleaned_data['password']
    user = authenticate(username=uname, password=upass)
    if user is not None:
     dj_login(request,user)
     messages.success(request, 'Logged in Successfully !!')
     return HttpResponseRedirect('/dashboard/')
  else:
   form = LoginForm()
  return render(request, 'blog/login.html', {'form':form})
 else:
  return HttpResponseRedirect('/dashboard/')




def logout(request):
 dj_logout(request)
 return HttpResponseRedirect('/')


def addpost(request):
 if request.user.is_authenticated:
  if request.method == 'POST':
   form = PostForm(request.POST)
   if form.is_valid():
    title = form.cleaned_data['title']
    desc = form.cleaned_data['desc']
    pst = Post(title=title, desc=desc)
    pst.save()
    form = PostForm()
  else:
   form = PostForm() # eitukur jonno addpost.htm e form ta dekha jay
  return render(request, 'blog/addpost.html', {'form':form})
 else:
  return HttpResponseRedirect('/login/')


def dashboard(request):
 if request.user.is_authenticated:
  posts = Post.objects.all()
  user = request.user
  full_name = user.get_full_name()
  gps = user.groups.all()
  return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
 else:
  return HttpResponseRedirect('/login/')


def update_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(pk=id)
      form = PostForm(request.POST, instance=pi)
      if form.is_valid():
        form.save()
    else:
      pi = Post.objects.get(pk=id)
      form = PostForm(instance=pi)
    return render(request, 'blog/updatepost.html', {'form':form})
  else:
    return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pi = Post.objects.get(pk=id)
      pi.delete()
      return HttpResponseRedirect('/dashboard/')
  else:
    return HttpResponseRedirect('/login/')

