from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SearchProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(SearchProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control', 'id':'title', 'class':'search_form', 'placeholder':'Search for products'})



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form form-control form-control-lg border-left-0', 'placeholder': 'username',})
        self.fields['first_name'].widget.attrs.update({'class' : 'form form-control px-5', 'placeholder' : 'Firstname', 'id':'floatingInput',})
        self.fields['last_name'].widget.attrs.update({'class' : 'form form-control px-5', 'placeholder' : 'Surname', 'id':'floatingInput',})                              
        self.fields['email'].widget.attrs.update({'class' : 'form form-control px-5', 'placeholder': 'Email',})
        self.fields['password1'].widget = forms.PasswordInput() 
        self.fields['password2'].widget.attrs.update({'class' : 'form form-control px-4 pb-3', 'placeholder':'Password', 'id':'password', })                        



class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':' Username', 
                                                    'class':'form form-control px-5 ', 'id':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 
                                                    'class':'form form-control px-5', 'id':'password',}))

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','slug', 'category','detail','specs', 'color','size','price','digital','image')
    
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['slug'].widget.attrs.update({'class' : 'form-control'})
        self.fields['category'].widget.attrs.update({'class' : 'form-control'})
        self.fields['detail'].widget.attrs.update({'class' : 'form-control'})
        self.fields['specs'].widget.attrs.update({'class' : 'form-control'})
        self.fields['color'].widget.attrs.update({'class' : 'form-control'})
        self.fields['size'].widget.attrs.update({'class' : 'form-control'})
        self.fields['price'].widget.attrs.update({'class' : 'form-control'})
        self.fields['digital'].widget.attrs.update({'class' : 'form-control'})
        self.fields['image'].widget.attrs.update({'class' : 'form-control'})


class AddProductColor(forms.ModelForm):
    class Meta:
        model = Color
        fields = {'title','color_code'}
    
    def __init__(self, *args, **kwargs):
        super(AddProductColor,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['color_code'].widget.attrs.update({'class' : 'form-control'})


class AddProductSize(forms.ModelForm):
    class Meta:
        model = Size
        fields = {'title'}

    def __init__(self, *args, **kwargs):
        super(AddProductSize,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        

class AddProductCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = {'title'}
    
    def __init__(self, *args, **kwargs):
        super(AddProductCategory,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})


class ContactUsForm(forms.ModelForm): 
    class Meta:
        model = Message
        fields = {'name','email','subject','message'}

    def __init__(self, *args , **kwargs):
        super(ContactUsForm,self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'form-control','placeholder':'Name', })
        self.fields['email'].widget.attrs.update({'class' : 'form-control','placeholder':'Email', })
        self.fields['subject'].widget.attrs.update({'class' : 'form-control','placeholder':'Subject', })
        self.fields['message'].widget.attrs.update({'class' : 'form-control','placeholder':'Message', })

