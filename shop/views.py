import json
import datetime
from .models import * 
from .forms import  *
from typing import OrderedDict
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login as user_login, logout as user_logout
from django.core.mail import send_mail

# Create your views here.

def Store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all().order_by('-date_created')[:6]
	page_number = request.GET.get('page')
	product_paginator = Paginator(products , 3)
	page = product_paginator.get_page(page_number)

	search_form = SearchProductForm()

	context={ 
        'items':items,
        'order':order,
        'cartItems':cartItems,
		'search_form':search_form,
		'count':product_paginator.count,
		'page':page
       
    }
	return render(request,'core/index.html', context)
    

def Cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={
        'items':items,
        'order':order,
        'cartItems':cartItems,
    }
    return render(request, "core/shopping-cart.html",context)
 

def Checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items':items,
        'order':order, 
        'cartItems':cartItems
        }
    return render (request, 'core/checkout.html',context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = CartOrder.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = CartOrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = CartOrder.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order, orderItem, item_title,item_quantity = guestOrder(request, data)
	
	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
        phone=data['shipping']['phone'],
		zipcode=data['shipping']['zipcode'],
		)
        

	if order.shipping == True and  order.complete == True:
		customer_order=[]
		for i in range(len(item_title)):
			a = item_title[i] + item_quantity[i]
			customer_order.append(a)
			
		formatted_customer_order =	 ' , '.join(customer_order)

		customer_phone = order.customer.phone
		customer_name =order.customer.name
		customer_mail = order.customer.email
		shipping_address=''.join(data['shipping']['address'])
		shipping_city=''.join(data['shipping']['city'])
		shipping_state=''.join(data['shipping']['state'])
		shipping_phone=''.join(data['shipping']['phone'])
		shipping_zipcode=''.join(data['shipping']['zipcode'])
		total = str(total)
		
		#customizing email
		subject = " Summary of order from ecommerce website"
		body =  'customer name =',customer_name ,'\n', 'Customers Address =', shipping_address,'\n','Customers Phone =',shipping_phone,'\n','Customers State =',shipping_state ,'\n','Customers City =',shipping_city,'\n','Customers ZIP Code =',shipping_zipcode ,'\n','ORDERED ITEMS AND QUANTITY =',formatted_customer_order, '\n','TOTAL AMOUNT PAYABLE = #'+ total,'\n',
		message = ' '.join(body)
		send_mail(subject, message, customer_mail,['ucktech1@gmail.com', customer_mail])
	return JsonResponse('Payment submitted..', safe=False)


def ContactUs(request):
	if request.method == "POST":
		contact_form = ContactUsForm(request.POST)
		if contact_form.is_valid():
			cd = contact_form.cleaned_data
			get_name = cd['name']
			get_email = cd['email']
			get_subject = cd['subject']
			get_message =cd['message']			
			send_mail(get_subject,get_message, get_email, ['ucktech1@gmail.com', get_email])

			contact_form.save()
			messages.success(request, ('message successfuly sent!'))
			return redirect('contact')
		else:
			messages.error(request, ('Message not sent Checkform.'))
	else:
		contact_form = ContactUsForm()
		context = {
			'contact_form':contact_form,
		}
	return render(request, 'core/contact.html', context)


def AboutUs(request):
	return render(request,'core/about.html')


@login_required
def Dashboard(request):
	user = request.user
	total_shop_items = Product.objects.all()
	total_customer = Customer.objects.all()
	customers = Customer.objects.all()
	total_order = CartOrder.objects.all()
	context = {
		'user':user,
		'total_shop_items':total_shop_items.count(),
		'total_customer':total_customer.count(),
		'customers':customers,
		'total_order':total_order.count()
	}
	return render(request, 'dashboard/dashboard.html',context)


def AdminLogin(request):
	if request.method =='POST':
		form = SignInForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
			if user is not None:
				user_login(request, user)
				return redirect('dashboard')
			else:
				form = SignInForm()
				messages.error(request, ('incorrect username or password!'))
				context = {
                        'form':form,
                    }
				return render (request,'dashboard/login.html', context)
		else:
			form = SignInForm()
			messages.error(request, ('incorrect username or password!'))
			context = {
                    'form':form,
                }
			return  render(request, "dashboard/login.html", context)
	else:
		form = SignInForm()
		context = {
            'form':form,
        }
		return  render(request, "dashboard/login.html", context)
	


def AdminSignup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = SignUpForm()
		messages.error(request, ('OOPS Something went wrong user was not created!'))
		context={
			'form':form
		}
	return render(request,'dashboard/register.html',context)


def AdminLogout(request):
	user_logout(request)
	return  redirect("store")
    

def AddProduct(request):
	if request.method =='POST':
		form = AddProductForm(request.POST,request.FILES) 
		if form.is_valid():
			try:
				form.save()
				messages.success(request, ('Product Added successfully'))
				return redirect("addproduct")
			except:
				messages.success(request, ('product was not added check the form'))	
		else:
			return render(request,'dashboard/addproduct.html',{'form' : form})
	else:
		form = AddProductForm()
		context = {
            'form':form,
        }
		return render(request, "dashboard/add_product.html", context)



def AddProduct_Color(request):
	if request.method =='POST':
		color_form = AddProductColor(request.POST)
		if color_form.is_valid():
			try:
				color_form.save()
				messages.success(request, ('color saved!'))
				return redirect("addproductcolor")
			except:
				messages.error(request, ('Color was not saved'))
		else:
			return render(request,'dashboard/addproduct.html',{'color_form' : color_form})
	else:
		color_form = AddProductColor()
		cat_form = AddProductCategory()
		size_form = AddProductSize()
		context = {
            'color_form':color_form,
			'cat_form':cat_form,
			'size_form':size_form 
        }
		return render(request, "dashboard/add_product_acc.html", context)



def AddProduct_Category(request):
	if request.method =='POST':
		cat_form = AddProductCategory(request.POST, request.FILES)
		if cat_form.is_valid():
			try:
				cat_form.save()
				messages.success(request, ('Category Created successfully'))
				return redirect("addproductcolor")
			except:
				messages.error(request, ('category not created!'))
		else:
			return render(request,'dashboard/addproduct.html',{'cat_form' : cat_form})
	else:
		cat_form = AddProductCategory()

		context = {
            'cat_form':cat_form,
        }
		return render(request, "dashboard/add_product_acc.html", context)


def AddProduct_Size(request):
	if request.method =='POST':
		size_form = AddProductSize(request.POST)
		if size_form.is_valid():
			try:
				size_form.save()
				messages.success(request, ('Product Size Created successfully'))
				return redirect("addproductcolor")
			except:
				messages.error(request, ('Product Size was not created! '))
			
		else:
			return render(request,'dashboard/addproduct.html',{'size_form' : size_form})
	else:
		size_form = AddProductSize()
		context = {
            'size_form':size_form,
        }
		return render(request, "dashboard/add_product_acc.html", context)


def EditProduct(request,pk):
	if request.method == 'POST':
		product= Product.objects.get(pk=pk)
		productForm = AddProductForm(request.POST, request.FILES, instance=product)
		
		if productForm.is_valid():
			 productForm.save()
			 messages.success(request, ('course was successfully updated!'))
			 return redirect('allproduct')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		product = Product.objects.get(pk=pk)
		productForm = AddProductForm(instance=product)
		
		context={
			'form':productForm,
        }
		return render(request,"dashboard/edit_product.html",context)


def DeleteProduct(request,pk):
	Product.objects.filter(pk=pk).delete()
	return redirect('allproduct')


def AllProduct(request):
	products = Product.objects.all().order_by('-date_created')[:6]
	page_number = request.GET.get('page')
	product_paginator = Paginator(products , 3)
	page = product_paginator.get_page(page_number)
	
	search_form = SearchProductForm()
	context  = {
		'count':product_paginator.count,
        'search_form':search_form,
        'page':page,
    }
	return render(request, "dashboard/all_products.html", context)



def SearchProduct(request):
    if request.method == "POST":
        searched = request.POST['title']
        user_search = Product.objects.filter(title__icontains = searched)
        form = SearchProductForm()
        
        #pagination
        page_number = request.GET.get('page')
        search_paginator = Paginator(user_search, 1)
        page = search_paginator.get_page(page_number)
    
        context = {
            'count': search_paginator.count,
            'searched':searched,
            'page':page,
            'form':form,
        }
        return render(request, "dashboard/product_search_result.html", context)
    else:
        
        return render(request, "dashboard/product_search_result.html")
         

