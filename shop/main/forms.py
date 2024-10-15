from asyncio import TaskGroup

from .models import  Product
from django import forms
from django.forms import ModelForm, TextInput, Textarea

mood_choices = [
        ('1', 'Melancholic'),
        ('2',  'Wild'),
        ('3',  'Funny'),
        ('3',  'Morally Gray'),
    ]

class ProductForm(forms.ModelForm):
    #title  = forms.CharField(label="title", max_length=50)
    #price = forms.IntegerField(label='price')
    #description = forms.Textarea()
    class Meta:
        model = Product
        fields = ['title', 'price']
        mood = forms.ChoiceField(widget=forms.RadioSelect(), choices=mood_choices)
        """
        widgets={
            'title': forms.CharField(label="title", max_length=50),
            'price':forms.CharField(label="title", max_length=50),
            'description':forms.Textarea(attrs={'cols':50,'rows':25}),
            'mood':forms.CheckboxInput()
        }"""



class LikeForm(forms.Form):

