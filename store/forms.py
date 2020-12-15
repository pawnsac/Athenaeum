from django import forms

class SearchForm(forms.Form):
    search_text = forms.CharField(label='SeachBar', max_length=100)

