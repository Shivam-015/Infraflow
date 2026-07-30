from django.urls import path
from . import views
urlpatterns = [
    
    path('login/' , views.user_login , name="login"),
    path('logout/',views.logout, name="logout"),
    path('register/',views.register,name="register"),
    path('delete-account/' , views.delete_account , name="delete_account"),
    path('profile/',views.profile,name="profile"),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name="payment_cancel"),
    path( 'address/' , views.address , name="address" ),
    path( 'add_address/' , views.add_address , name="add_address" ),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('my-orders/', views.order_history, name='my_orders'),
    path('track-order<int:order_id>/' , views.track_order , name='track_order'),
    path('delete_address<int:address>/' , views.delete_address , name="delete_address"),
    
]
