from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from users.forms import ThreadForm, MessageForm
from .models import Post, ThreadModel, MessageModel, Notification
from django.shortcuts import redirect

@login_required
def favourite_list(request):
    new = Post.objects.filter(favourites=request.user)
    return render(request,
                  'blog/favourites.html',
                  {'new': new})

@login_required
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by =  5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by =  5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'price', 'locality', 'superficy', 'Type_of_property', 'content', 'image']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form_update.html'
    fields = ['title', 'price', 'locality', 'superficy', 'Type_of_property', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def localisation(request):
 return render(request, 'blog/localisation.html')

def graphic(request):
 return render(request, 'blog/graphic.html')




@login_required()
def search_post(request):
    search = request.GET.get('search')
    posts = Post.objects.filter(Q(title__icontains=search) |
                                Q(content__icontains=search) |
                                Q(locality__icontains=search)|
                                Q(price__icontains=search))

    posts_number = posts.count()

    message = f'{posts_number} results :'

    if posts_number == 1:
        message = f'{posts_number} result :'


    context = {
        'posts' : posts,
        'message': message,
    }

    return render(request, 'blog/search_post.html', context)



class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user = request.user) |
                                             Q(receiver= request.user))

        context = {
            'threads' : threads
        }
        return render(request, 'blog/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form' : form
        }
        return render(request, 'blog/create_thread.html', context)
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        try :
            receiver = User.objects.get(username= username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists() :
               thread = ThreadModel.objects.filter(user = request.user, receiver=receiver)[0]
               return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user = receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user )[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user = request.user,
                    receiver = receiver
                )
                thread.save()
                return redirect('thread', pk = thread.pk)
        except:
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread' : thread,
            'form' : form,
            'message_list' : message_list
        }

        return render(request, 'blog/thread.html', context)





class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else :
            receiver = thread.receiver

        message = MessageModel(
            thread = thread,
            sender_user = request.user,
            receiver_user = receiver,
            body = request.POST.get('message')
        )

        message.save()

        notification = Notification.objects.create(
            notification_type=1,
            from_user=request.user,
            to_user=receiver,
            thread = thread
        )
        return redirect('thread', pk=pk)



class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

