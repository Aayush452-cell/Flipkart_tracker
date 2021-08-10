from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.signup,name='signup'),
    path('index/', views.home,name='home'),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('signin/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path('add_items/',views.add_items,name="add_items"),
    path('delete_item/<int:id>',views.delete_item,name='delete_item'),
    path('search/', views.search, name="search"),
    path('update/', views.update, name="update"),
]