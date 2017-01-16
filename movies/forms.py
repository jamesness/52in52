from django import forms

from django.contrib.admin import widgets

class MovieSearchForm(forms.Form):
	view_date = forms.DateField(widget = widgets.AdminDateWidget)