from django import forms

class FormSearch(forms.Form):
    subcategory_id = forms.IntegerField(required=False, initial=0)
    name = forms.CharField(required=False, max_length=100)