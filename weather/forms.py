from django import forms

class CitySearchForm(forms.Form):
    city = forms.CharField(label="Введите город", max_length=100)
