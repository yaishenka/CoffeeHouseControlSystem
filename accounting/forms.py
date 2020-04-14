from django import forms
from .models import Purchase, OrderPiece

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('order_positions', )


class OrderPieceForm(forms.ModelForm):
    forms.CharField()
    class Meta:
        model = OrderPiece
        fields = ('product', 'count')
