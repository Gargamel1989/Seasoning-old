from django import forms

class SearchIngredientForm(forms.Form):
    
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zoek Ingredienten', 'class': 'keywords-searchbar'}))