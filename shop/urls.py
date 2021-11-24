from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.Store, name="store"),
	path('about/', views.AboutUs, name="about"),
	path('contact/', views.ContactUs, name="contact"),
	path('cart/', views.Cart, name="cart"),
	path('checkout/', views.Checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('dashboard/', views.Dashboard, name="dashboard"),
    path('dashboard/register/', views.AdminSignup, name='signup'),
	path('dashboard/login/', views.AdminLogin, name='login'),
	path('dashboard/logout/', views.AdminLogin, name='logout'),
	path('dashboard/addproduct/', views.AddProduct, name='addproduct'),
	path('dashboard/editproduct/<int:pk>/', views.EditProduct, name='editproduct'),
	path('dashboard/deletproduct/<int:pk>/', views.DeleteProduct, name='deleteproduct'),
	path('dashboard/allproduct/', views.AllProduct, name='allproduct'),
	path('dashboard/product_search_result/', views.SearchProduct, name='searchproduct'),
	path('dashboard/addproductcolor/', views.AddProduct_Color, name='addproductcolor'),
	path('dashboard/addproductsize/', views.AddProduct_Size, name='addproductsize'),
	path('dashboard/addproductcategory/', views.AddProduct_Category, name='addproductcategory'),

    
    
]