from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    # path('login', views.login, name='login'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('orders', views.orders, name='orders'),
    path('getallproducts', views.getAllProducts, name='getallproducts'),
    path('getproduct/<int:pk>', views.getProduct, name="getproduct"),
    path('demo', views.demo, name="demo"),
]
