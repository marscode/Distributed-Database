from django import forms
from .models import Product, LoginTracker
from django.core.exceptions import ValidationError
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.models import User

user = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Admin', widget=forms.Textarea, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise ValidationError(_('Username or Password is incorrect'))

class ProductForm(forms.ModelForm):
    category = forms.CharField(max_length=50)
    product_name = forms.CharField(max_length=50)
    quantity = forms.IntegerField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)


    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']

        if Product.objects.filter(product_name=product_name):
            raise forms.ValidationError('Cannot Add duplicated products')
        return product_name


    class Meta:
        model = Product
        fields = ('category', 'product_name', 
                  'quantity', 'price', 
                  )


