from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Quantity allows the user to select a quantity b/w 1 & 20. we use a typedchoicefield 
    w/ coerce=int to convert the input into an integer. | Override allows us to indicate whether
    the q has to be added to any existing q in cart for this product F or whether the existing q 
    has to be overridden w/ the given q T"""
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Quantity'))
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
