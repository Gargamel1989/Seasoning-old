"""
Copyright 2012, 2013 Driesen Joep

This file is part of Seasoning.

Seasoning is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Seasoning is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Seasoning.  If not, see <http://www.gnu.org/licenses/>.
    
"""
# Based on django-ajax-selects from crucialfelix
from django import forms
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from ingredients.models import Ingredient

class AutoCompleteSelectIngredientWidget(forms.widgets.TextInput):

    def render(self, name, value, attrs=None):
        value = value or ''
        if value:
            try:
                ingredient_pk = int(value)
                value = Ingredient.objects.get(pk=ingredient_pk).name
            except ValueError:
                # If we cannot cast the value into an int, it's probably the name of
                # the ingredient already, so we don't need to do anything
                pass
            except ObjectDoesNotExist:
                raise Exception("Cannot find ingredient with id: %s" % value)
        return super(AutoCompleteSelectIngredientWidget, self).render(name, value, attrs)
    
class AutoCompleteSelectIngredientField(forms.fields.CharField):

    """
    Form field to select a model for a ForeignKey db field
    """

    def __init__(self, *args, **kwargs):
        widget = kwargs.get('widget', False)
        if not widget or not isinstance(widget, AutoCompleteSelectIngredientWidget):
            kwargs['widget'] = AutoCompleteSelectIngredientWidget()
        super(AutoCompleteSelectIngredientField, self).__init__(*args, **kwargs)
        
    def clean(self, value):
        if value:
            try:
                ingredient = Ingredient.objects.get(name__exact=value)
            except MultipleObjectsReturned:
                raise forms.ValidationError(u"Multiple result returned for ingredient name: %s" % value)
            except ObjectDoesNotExist:
                raise forms.ValidationError(u"No ingredient found with name: %s" % value)
            return ingredient
        else:
            if self.required:
                raise forms.ValidationError(self.error_message['required'])
            return None
