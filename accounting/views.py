from django.shortcuts import render, get_object_or_404, redirect
from .forms import PurchaseForm, OrderPieceForm
from django.http import HttpResponseRedirect
from .decorators import seller_rights_required, manager_rights_required
from django.urls import reverse
from .models import Purchase


@seller_rights_required
def create_purchase(request):
    new_purchase = Purchase(seller=request.user)
    new_purchase.save()
    print("HERE")
    return redirect('add_position', purchase_uid=new_purchase.uid)


@seller_rights_required
def view_purchase(request, purchase_uid):
    purchase = get_object_or_404(Purchase, uid=purchase_uid)
    return render(request, 'purchases/view.html', {'purchase': purchase})



@seller_rights_required
def add_order_position(request, purchase_uid):
    if request.method == 'POST':
        order_piece_form = OrderPieceForm(request.POST)
        if order_piece_form.is_valid():
            new_order_piece = order_piece_form.save(commit=True)
            purchase_object = Purchase.objects.all().get(uid=purchase_uid)
            purchase_object.order_positions.add(new_order_piece)
            purchase_object.save()
            return redirect('view_purchase', purchase_uid=purchase_object.uid)
    else:
        order_piece_form = OrderPieceForm()
    return render(request, 'purchases/create.html', {'form': order_piece_form})


@manager_rights_required
def view_all_purchases(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchases/list.html', {'purchases': purchases})
