

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),
    path('busket', views.busket, name='busket'),
    path('<int:id>/make_order/', views.make_order, name="make_order"),
    #path('sign_in', views.sign_in, name='sign_in'),
    path('add_product', views.add_product, name='add_product'),
    #path('<int:id>/', views.product_detail, name = 'product_detail'),
]
