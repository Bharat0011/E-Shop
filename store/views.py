from django.shortcuts import render, HttpResponse,redirect
from .models import Product, Category, Customer, Order
# from django.contrib.auth.hashers import make_password, check_password
from .serializer import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method =='GET':
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        categories = Category.get_all_categories()

        category_ID = request.GET.get('category')
        if category_ID:
            products = Product.get_all_products_by_category_id(category_id=category_ID)
        else:
            products = Product.get_all_products()

        data = {}
        data['products'] = products
        data['categories'] = categories
        print("GET request index cname",request.session.get('user'))
        return render(request, 'index.html', data)
    
    else:
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print("Index in POST request cart",request.session['cart'])
        return redirect('home')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # values = {
        #     'first_name' : first_name, 'last_name' : last_name,
        #     'phone' : phone, 'email' : email,
        # }
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        customer = Customer(user = myuser, phone = phone)
        customer.save()
        messages.success(request, "Your account has been successfully created !!")
        return redirect('login')

        # myuser.phone = phone
        # customer = Customer(first_name=first_name, last_name = last_name, phone = phone, email = email, password = password)
        
        # if customer.isExists():
        #     error = 'Email is already registered'
        #     data = {
        #         'error' : error,
        #         'values' : values
        #     }
        #     return render(request, 'signup.html', data)
        # else:
        #     customer.password = make_password(customer.password)
        #     customer.register()
        #     return redirect('login')

    return render(request, 'signup.html')


# login using auth
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print("NOT NONE")
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in..."))
            print("NONE")
            return redirect('login')

    return render(request, 'login.html')


def demo(request):
    if request.method == "POST":
        data = request.POST.get('data')
        print(data)
        return render(request, 'demo.html')
    return render(request, 'demo.html')















# login using session
# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')


#         customer = Customer.get_customer_by_email(email)
        
        
#         if customer:
#             flag = check_password(password, customer.password)
#             if flag:
#                 request.session['customer'] = customer.id
#                 request.session['customer_name'] = customer.first_name
#                 print(request.session['customer_name'])
#                 return redirect('home')
#             else:
#                 error_msg = "Email or Password is invalid !"
#         else:
#             error_msg = "Email or Password is invalid !"
        
#         return render(request, 'login.html', {'error':error_msg})


    # return render(request, 'login.html')

#logout using auth,logout
def logout_user(request):
    logout(request)
    return redirect('home') 

#logout using session
# def logout(request):
#     request.session.clear()
#     return redirect('login')

def cart(request):
    if request.method =='GET':
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
            return render(request, 'cart.html')
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    print(products)
    return render(request, 'cart.html', {'products':products})


def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.user.id
        if not customer:
            messages.success(request, "Please Login to place your order")
            return redirect('login')
        print("Customer", customer)
        cart = request.session.get('cart')
        if not cart:
            messages.success(request, "Not product is added in the cart")
            return redirect('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(products)

        for product in products:
            order = Order(product = product ,customer = Customer.objects.get(user= customer), quantity = cart.get(str(product.id)), price = product.price, address = address, phone = phone)
            order.save()

        request.session['cart'] = {}
        return redirect('cart')


@login_required(login_url='login')
def orders(request):
    customer = Customer.objects.get(user= request.user.id)
    orders = Order.objects.filter(customer = customer).order_by('-date')
    print("ORDERS ", orders)
    return render(request, 'orders.html', {'orders':orders})










@api_view(['GET'])
def getAllProducts(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id = pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
    
