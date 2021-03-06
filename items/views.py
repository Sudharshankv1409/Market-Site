from django.shortcuts import render
from django.views import View
from .models import Item
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

class CategoryPage(View):
    def get(self, request):
        items = Item.objects.all()
        return render(request,'items/category.html',context = {'items':items})

class CartPage(LoginRequiredMixin,View):
    def get(self, request):
        carts = Cart.objects.filter(user=request.user).select_related('item','user')
        return render(request,'items/cart.html',{'carts':carts})

    def post(self, request):
        user = request.user
        item = int(request.POST.get('item'))
        item = Item.objects.get(pk=item)
        try:
            cart = Cart.objects.get(user=user, item=item)
            messages.warning(request,'Already added to the cart')
            return JsonResponse({
                'status':'Already added to the cart'
            })
        except:
            if item:
                messages.warning(request,'Successfully added to the cart')
                data = {
                    'status':'success'
                }
                quantity = 1
                cart = Cart.objects.create(user = user, item = item, item_quantity = quantity)
                cart.save()
                return JsonResponse(data)

class CartUpdatePage(LoginRequiredMixin,View):
    def post(self, request):
        pk = request.POST.get('pk')
        value = int(request.POST.get('value'))
        cart = Cart.objects.get(pk=pk)
        if value:
            cart.item_quantity = value
            cart.save()
        else:
            cart.delete()
        return JsonResponse({
                'status':'success'
        })

class CheckoutPage(LoginRequiredMixin, View):
    def get(self, request):
        carts = Cart.objects.filter(user=request.user).select_related('item','user')
        total_cost = 0
        for i in carts:
            total_cost += i.item_quantity * i.item.revised_cost
        context = {'carts':carts, 'total_cost':total_cost}
        return render(request,'items/checkout.html', context)
