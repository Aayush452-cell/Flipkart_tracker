from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,  login, logout
from .utils import get_url_link
from .models import Link
import smtplib

# Create your views here.

def sendmail(item):
    '''Function called when the email needs to be sent '''
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('@gmail.com', '')

    url = ""
    subject = 'Hey! Price fell down of the ' + item.name + 'on Flipkart'
    body = 'Check the link ' + url + 'Now the lowest price ever is : Rs' + str(item.lowest_price) + '. With price drop of : Rs ' + str(item.price_difference)

    msg = f"Subject: {subject}\n\n{body}"

    user =item.user
    user_mail = User.objects.get(username=user).email
    server.sendmail('@gmail.com', user_mail , msg)

    print('Email Sent')

    server.quit()

def items_update():
    items = Link.objects.all()
    for item in items:
        name, price = get_url_link(item.url)
        item.old_price = item.current_price
        item.current_price = price
        if price < item.lowest_price:
            item.lowest_price = price
        item.price_difference = item.current_price - item.old_price
        if item.old_price < item.current_price:
            sendmail(item)
        item.save()

def update(request):
    items_update()
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        prods = Link.objects.filter(user=request.user)
        items_no = prods.count()
        no_discounted = 0
        if items_no > 0:
            discount_list = []
            for item in prods:
                if item.old_price > item.current_price:
                    discount_list.append(item)
            no_discounted = len(discount_list)
        context = {
            'prods':prods,
            'items_no':items_no,
            'no_discounted':no_discounted,
        }
        return render(request, 'flipkart_tracker/index.html', context)
    else:
        messages.error(request, "Sign in First !")
        return redirect('signup')

def signup(request):
    return render(request, 'flipkart_tracker/signup.html')

def add_items(request):
    if request.method == "POST":
        try:
            link = request.POST['link']
            name, price = get_url_link(link)
            url = link
            user = request.user
            current_price = price
            old_price = price
            lowest_price = price
            price_difference = 0
            item = Link(name=name, url=url, user=user, current_price=current_price, old_price=old_price,
                        lowest_price=lowest_price,
                        price_difference=price_difference)
            item.save()
        except AttributeError:
            messages.error(request," Ups...couldn't get the product there might be something wrong with the network please try again!")
        except:
            messages.error(request, "Ups...couldn't get the product there might be something wrong with the network please try again!")
        return redirect('home')

def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm password']

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return render(request, 'flipkart_tracker/signup.html')

        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return render(request, 'flipkart_tracker/signup.html')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, " Your Account has been successfully created")
        return render(request, 'flipkart_tracker/signup.html')

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['username']
        loginpassword = request.POST['password']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return render(request, 'flipkart_tracker/signup.html')

    return HttpResponse("404- Not found")

def delete_item(request,id):
    if request.method == 'POST':
        try:
            item = Link.objects.filter(id=id)
            item.delete()
            messages.success("Item has been removed successfully !")
        except:
            messages.error(request, "something went wrong please try again !")
    return redirect('home')

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request, 'flipkart_tracker/signup.html')

def searchMatch(query, item):
    if query in item.name:
        return True
    else:
        return False

def search(request):
    query = request.GET['query']
    prodst = Link.objects.filter(user=request.user)
    items_no = prodst.count()
    no_discounted = 0
    if items_no > 0:
        discount_list = []
        for item in prodst:
            if item.old_price > item.current_price:
                discount_list.append(item)
        no_discounted = len(discount_list)
    prods = []
    allprods = Link.objects.filter(user=request.user)
    for item in allprods:
        if searchMatch(query, item):
            prods.append(item)

    context = {
        'prods': prods,
        'query': query,
        'items_no':items_no,
        'no_discounted':no_discounted,
    }
    return render(request, 'flipkart_tracker/search.html', context)
