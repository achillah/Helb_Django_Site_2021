from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    ListThreads,
    CreateThread,
    ThreadView,
    CreateMessage,
    ThreadNotification,
    RemoveNotification,

)
from . import views 

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), #localhost:8000/blog/
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/localisation/', views.localisation, name='post-localisation'),
    path('post/graphic/', views.graphic, name='graphic'),
    path('search_post/', views.search_post, name= 'search_post'),
    path('post/fav/<int:id>', views.favourite_add, name = 'favourite_add'),
    path('post/favourites/', views.favourite_list, name='favourite_list'),
    path('inbox/', ListThreads.as_view(), name = 'inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message', CreateMessage.as_view(), name = 'create-message'),
    path('notification/<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),

]

