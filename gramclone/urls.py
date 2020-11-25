from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='MainPage'),
    path('search/', views.search_results, name='search_results'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.login, name='login'),
    path('add_image/', views.add_image, name='addImage'),
    path('my_timeline/', views.timeline, name='timeline'),
    path('<uuid:post_id>', views.single_post, name='singlePost'),
    path('<uuid:post_id>/like', views.like, name='likePost'),
    path('profile/<username>', views.user_profile, name='profile'),
    path('profile/<username>/create', views.profile_form, name='createProfile'),
    path('profile/<username>/edit', views.profile_edit, name='editProfile'),
    path('profile/<username>/follow/<option>', views.follow, name='follow'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
