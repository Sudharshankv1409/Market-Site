from django.urls import path
from . import views
app_name = 'items'

urlpatterns = [
    path('saree/cotton',views.CategoryPage.as_view(),name = 'category'),
    path('cart/',views.CartPage.as_view(),name = 'cart'),
    path('update_cart/',views.CartUpdatePage.as_view(), name = 'update_cart'),
    path('checkout/',views.CheckoutPage.as_view(), name = 'checkout'),
]
