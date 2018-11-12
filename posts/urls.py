from django.urls import path

from posts import views
app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('<int:id>', views.details, name='details'),
    path('<int:id>/upvote', views.upvote, name='upvote'),
    path('<int:id>/downvote', views.downvote, name='downvote'),
    path('<int:post_id>/comments/<int:node_id>/upvote', views.comment_upvote, name='comment_upvote'),
    path('<int:post_id>/comments/<int:node_id>/downvote', views.comment_downvote, name='comment_downvote'),
    path('<int:post_id>/comments/reply/<int:parent_id>', views.comment_reply, name='comment_reply'),
]