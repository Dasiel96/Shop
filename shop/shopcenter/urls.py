from django.urls import path
from . import views, ajax

urlpatterns = [
    path('', views.login, name="shop-login"),
    path('featured/', views.featured, name="shop-featured"),
    path('item/', views.item, name="shop-item"),
    path('cart/', views.cart, name="shop-cart"),
    path('checkout/', views.checkout, name="shop-checkout"),
    path('furn/', views.shopFurniture, name="shop-furn"),
    path("elec", views.shopElectronics, name="shop-elec"),
    path("otdr/", views.shopOutDoors, name="shop-otdr"),
    path("ptsp/", views.shopPetSupplies, name="shop-ptsp"),
    path("spts/", views.shopSports, name="shop-spts"),
    path("toys/", views.shopToys, name="shop-toys"),
    path("search/", views.shopSearch, name="shop-search"),
    path("sources/", views.sources, name="shop-source"),
    path('ajax/item/', ajax.goToItem, name="ajax-go-to-item"),
    path('ajax/cart/', ajax.addToCart, name="ajax-add-cart"),
    path('ajax/removeItem/', ajax.removeCartItem, name="ajax-remove-cart"),
    path('ajax/empty/', ajax.emptyCart, name="ajax-empty-cart"),
    path('ajax/search/', ajax.recordSearch, name="ajax-record-search"),
    path('ajax/swapImg/', ajax.newImg, name="ajax-change-img"),
]