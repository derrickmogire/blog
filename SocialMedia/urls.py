from django.urls import path
from SocialMedia import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/<slug>',
         views.post_detail, name='details'),
    path('new_post/', views.createpost, name='newpost'),
    path('edit_profile/', views.edit_profile, name='editprofile'),
    path('likes/', views.like_post, name='like_post'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('editpost/<int:id>', views.edit_post, name='editpost'),
    path('deletepost/<int:id>', views.delete_post, name='deletepost'),
    path('favourites/<int:id>', views.favourite_post, name='favouritepost'),
    path('favourites/', views.favourite_posts_list, name='favourites'),
  

]
