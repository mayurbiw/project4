from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register",views.register_view, name="register"),
    path("profile",views.profile_view, name="profile"),
    path('selectCategories',views.selectCategories_view,name="selectCategories"),
    path('followCategory/<category>',views.followCategory_view,name="followCategory"),
    path('unfollowCategory/<category>',views.unfollowCategory_view,name="unfollowCategory"),
    path('changePassword',views.changePassword,name="changePassword"),
    path('fetchNews',views.fetchNews,name="fetchNews"),
    path('readLater',views.readLater,name="readLater"),
    path('fetchSearchedNews',views.fetchSearchedNews,name="fetchSearchedNews"),

]
