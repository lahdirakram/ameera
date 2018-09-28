from django import forms
from .models import Product

class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('prod_name', 'prod_image','prod_PU','prod_Q','prod_sell')

class Connect(forms.Form):

	user_name=forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label='Nom d\'utilisateur',max_length=100)
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),label='Password',max_length=100)
		