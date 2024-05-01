from django.urls import path
from . import views

urlpatterns = [
    path('gencc/', views.GenerateCouponCodes.as_view(), name='generate_code'),
    path('generate_coupon_code/success/', views.GenerateSuccess.as_view(), name='generate_success'),
    path('validate/code/', views.ValidateCouponCodes.as_view(), name='validate_code'),
]