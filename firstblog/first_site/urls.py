from django.urls import path
from first_site import  views
# app_name = 'first_site'

urlpatterns =[
path('',views.BaseView.as_view(),name='home'),
path('post/',views.PostListView.as_view(),name='post_list'),
path('about/',views.AboutView.as_view(),name='about'),
path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
path('new/post/',views.CreatePostView.as_view(),name='post_new'),
path('post/<int:pk>/edit/',views.PostUpdateView.as_view(),name='post_update'),
path('post/delete/<int:pk>/',views.PostDeleteView.as_view(),name='post_delete'),
path('drafts/',views.DraftListview.as_view(),name='post_draft_list'),
path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
path('comment/<int:pk>/approve/',views.comment_approve,name='comment_approve'),
path('comment/<int:pk>/remove/',views.comment_remove,name='comment_remove'),
path('post/<int:pk>/publish',views.post_publish,name='post_publish'),
]
