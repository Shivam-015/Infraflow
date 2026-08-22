from django.urls import path
from . import views
urlpatterns = [
    path('' , views.home , name="home"),
    path('products/' , views.all_products , name="all_products"),
    path('contact/' , views.contact , name="contact"),
  
    path('product_details/<int:product_id>', views.product_details , name="product_details"),
    path('cart/' , views.cart , name="cart"),
    path('delete_from_cart/<int:item_id>',views.delete_from_cart,name='delete_from_cart'),
    path('add_to_cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('increase<int:item_id>/' , views.increase , name="increase"),
    path('decrease<int:item_id>/' , views.decrease , name="decrease"),
    path('wishlist/' , views.wishlist , name="wishlist"),
    path('add-to-wishlist/<int:product_id>/' , views.add_to_wishlist , name="add_to_wishlist"),
    path('delete-from-wishlist/<int:product_id>/' , views.delete_from_wishlist , name="delete_from_wishlist"),
    path('buy_now/' , views.buy_now , name="buy_now"),
    path('about/' , views.about , name="about"),
    path( 'help_center/' , views.help_center , name='help_center'),
    path( 'terms_conditions/' , views.terms_conditions , name='terms_conditions'),
] 

