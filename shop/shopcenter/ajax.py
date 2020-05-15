from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from . import models
import json
from .views import MEDIA_PATH, readShoppingJson, writeShoppingJson, _LAST_URL_VISITED, _SEARCH_STR
from django.views.decorators.csrf import csrf_exempt
from random import randint




def isItemInCart(cart, item):
    is_in_cart = False
    for key in cart["cart"]:
        if cart["cart"][key]["name"] == item:
            is_in_cart = True
            break
    return is_in_cart
    

@csrf_exempt
def goToItem(responce):
    if responce.is_ajax():
        clicked_item = models.ShopItem.objects.filter(image=responce.POST["item_name"])
        cur_selected_item = models.ShopItem.objects.filter(was_clicked=True)

        if len(cur_selected_item):
            cur_selected_item[0].was_clicked = False
            cur_selected_item[0].save()

        if len(clicked_item) > 0:
            cur_item = len(clicked_item) - 1
            clicked_item[cur_item].was_clicked = True
            clicked_item[cur_item].save()

    x = redirect('shop-item')
    return HttpResponse(json.dumps({"url": x.url}), content_type="application/json")

@csrf_exempt
def addToCart(responce):
    if responce.is_ajax():
        cart = FileSystemStorage(location=MEDIA_PATH)
        key = "img_name"
        cart_as_json = {}

        with cart.open("shopping_info.json", "r") as f:
            try:
                cart_as_json = json.load(f)
            except:
                pass

        if not "cart" in cart_as_json:
            cart_as_json["cart"] = {}
        
        if not isItemInCart(cart_as_json, responce.POST[key]):
            cart_key = len(cart_as_json["cart"])
            cart_as_json["cart"][cart_key] = {
                "name": responce.POST[key],
                "amount": 1,
            }
        
        with cart.open("shopping_info.json", "w") as f:
            json.dump(cart_as_json, f)
    
    url = cart_as_json[_LAST_URL_VISITED]
    return HttpResponse(json.dumps({"url": url}), content_type="application/json")

@csrf_exempt
def removeCartItem(responce):
    if responce.is_ajax():
        cart = readShoppingJson()
        item = models.ShopItem.objects.filter(image=responce.POST["src"])[0]
        rm_key = None
        for key in cart["cart"]:
            img_name = cart["cart"][key]["name"]
            amt = int(cart["cart"][key]["amount"])
            if img_name == item.image:
                num_to_remove = int(responce.POST["num_to_remove"])
                if amt - num_to_remove > 0:
                    cart["cart"][key]["amount"] = str(amt - num_to_remove)
                else:
                    rm_key = key
                break
        if rm_key is not None:
            del cart["cart"][rm_key]
        writeShoppingJson(cart)
    return HttpResponse(json.dumps({"remove": rm_key is not None}), content_type="application/json")


@csrf_exempt
def emptyCart(responce):
    if responce.is_ajax():
        writeShoppingJson({"cart": {}, _LAST_URL_VISITED: "", _SEARCH_STR: ""})
    return HttpResponse()

@csrf_exempt
def recordSearch(responce):
    if responce.is_ajax():
        cart = readShoppingJson()
        cart[_SEARCH_STR] = responce.POST[_SEARCH_STR]
        writeShoppingJson(cart)
    url_search = redirect('shop-search').url
    return HttpResponse(json.dumps({"url": url_search}), content_type="application/json")


@csrf_exempt
def newImg(responce):
    url = 0
    if responce.is_ajax():
        items = models.ShopItem.objects.all()
        new_item = randint(0, len(items)-1)
        url = f"/static/shop/media/images/{items[new_item].image}"
    return HttpResponse(json.dumps({"url": url}), content_type="application/json")