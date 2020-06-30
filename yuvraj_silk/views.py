from django.shortcuts import render
from django.views import View
from items.models import Item

# Create your views here.

class IndexPage(View):
    def get(self,request):
        items = Item.objects.all()
        return render(request,'index.html',{'items':items})
