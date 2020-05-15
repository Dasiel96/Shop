from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.files.storage import FileSystemStorage
from .models import ShopItem
from random import randint
import json
import os


MEDIA_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/static/shop/media"
STATIC_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/static"

_TITLE_KEY = "title"
_LAST_URL_VISITED = "last url"
_SEARCH_STR = "search string"

def readShoppingJson():
    json_cart = {}
    fs = FileSystemStorage(location=MEDIA_PATH)
    with fs.open("shopping_info.json", "r") as f:
        try:
            json_cart = json.load(f)
        except:
            json_cart = {}
    return json_cart


def writeShoppingJson(json_obj):
    fs = FileSystemStorage(location=MEDIA_PATH)
    with fs.open("shopping_info.json", "w") as f:
        json.dump(json_obj, f)

def recordUrl(url):
    cart = readShoppingJson()
    cart[_LAST_URL_VISITED] = url
    writeShoppingJson(cart)

def shopDataBaseInit():
    fs = FileSystemStorage(location=MEDIA_PATH)
    shop_item_data = None
    with fs.open("items.json") as f:
        shop_item_data = json.load(f)

    print(len(ShopItem.objects.all()), len(shop_item_data["items"]))
    
    for item_data in shop_item_data["items"]:
        item_name = "name"
        item_catagory = "catagory"
        item_img = "img"
        item_src = "source"
        item_disc = "discription"
        item_price = "price"

        if len(ShopItem.objects.filter(source=item_data[item_src])) == 0:
            item = ShopItem(
                name=item_data[item_name], 
                item_cat=item_data[item_catagory],
                image=item_data[item_img],
                source=item_data[item_src], 
                discription=item_data[item_disc], 
                price=item_data[item_price],
                was_clicked=False
                )
            item.save()
    print("done")
    

def generateItemInfo(db_obj):
    image_path = "/static/shop/media/images"
    return {
        "img": f"{image_path}/{db_obj.image}",
        "img_name": db_obj.image, 
        "disc": db_obj.discription, 
        "price": db_obj.price, 
        "title": db_obj.name,
        "catagory": db_obj.item_cat,
        "src": db_obj.source
    }

def deselectItem():
    shopDataBaseInit()
    selected_item = ShopItem.objects.filter(was_clicked=True)
    print(len(selected_item))
    for item in selected_item:
        print("deselecting")
        item.was_clicked = False
        item.save()

def getNumOfItemsInCart():
    return len(readShoppingJson()["cart"])

def shoppingPage(request, cat_filter, page):
    items = ShopItem.objects.filter(item_cat=cat_filter)
    context_data = {
        _TITLE_KEY: cat_filter.upper(),
        "cart_size": getNumOfItemsInCart()
    }
    context_data["selection"] = []
    for item in items:
        context_data["selection"].append(generateItemInfo(item))
    
    return render(request, f"shopcenter/{page}.html", context_data)

# Create your views here.
def featured(request):
    deselectItem()

    pet_supplies = ShopItem.objects.filter(item_cat="pet supplies")
    electronics = ShopItem.objects.filter(item_cat="electronics")
    furniture = ShopItem.objects.filter(item_cat="furniture")
    outdoors = ShopItem.objects.filter(item_cat="outdoors")
    toys = ShopItem.objects.filter(item_cat="toys")
    sports = ShopItem.objects.filter(item_cat="sports")
    all_items = ShopItem.objects.all()

    top_pet_supply = randint(0, len(pet_supplies)-1)
    top_electronics = randint(0, len(electronics)-1)
    top_furn = randint(0, len(furniture)-1)
    top_outdoors = randint(0, len(outdoors)-1)
    top_all = randint(0, len(all_items)-1)
    top_toys = randint(0, len(toys)-1)
    top_sports = randint(0, len(sports) - 1)

    context = {
        _TITLE_KEY: "Featured",
        "top_ps": generateItemInfo(pet_supplies[top_pet_supply]),
        "top_ele": generateItemInfo(electronics[top_electronics]),
        "top_furn": generateItemInfo(furniture[top_furn]),
        "top_od": generateItemInfo(outdoors[top_outdoors]),
        "top_all": generateItemInfo(all_items[top_all]),
        "top_toy": generateItemInfo(toys[top_toys]),
        "top_sprt": generateItemInfo(sports[top_sports]),
        "cart_size": getNumOfItemsInCart(),
        "static": STATIC_PATH,
    }
    recordUrl(redirect("shop-featured").url)
    return render(request, 'shopcenter/featured.html', context)


def login(request):
    deselectItem()
    context = {
        _TITLE_KEY: "Login",
        "static": STATIC_PATH,
    }
    recordUrl(redirect("shop-login").url)
    return render(request, 'shopcenter/login.html', context)

def item(request):
    selected_item = ShopItem.objects.filter(was_clicked=True)
    context = {
        _TITLE_KEY: "Item",
        "cart_size": getNumOfItemsInCart(),
    }

    if(len(selected_item) > 0):
        context["selected"] = generateItemInfo(selected_item[0])
        suggested_items = ShopItem.objects.filter(item_cat=selected_item[0].item_cat)
        context["suggested"] = []
        for item in suggested_items:
            if len(context["suggested"]) == 10:
                break
            elif item.source != selected_item[0].source:
                context["suggested"].append(generateItemInfo(item))
    else:
        print("not found flagged")

    return render(request, 'shopcenter/item.html', context)

def cart(request):
    cart_file = FileSystemStorage(location=MEDIA_PATH)
    cart = None
    context = {
        _TITLE_KEY: "Cart",
        "cart_size": getNumOfItemsInCart(),
        "cart": [],
        "static": STATIC_PATH,
    }

    with cart_file.open("shopping_info.json", "r") as f:
        try:
            cart = json.load(f)
        except:
            cart = {}

    for key in cart["cart"]:
        item = ShopItem.objects.filter(image=cart["cart"][key]["name"])[0]
        amt = cart["cart"][key]["amount"]
        context["cart"].append({"amt": amt, "item": generateItemInfo(item)})
    
    recordUrl(redirect("shop-cart").url)

    return render(request, 'shopcenter/cart.html', context)

def checkout(request):
    context_data = {
        _TITLE_KEY: "Checkout",
        "cart_size": getNumOfItemsInCart()
    }
    cart_file = FileSystemStorage(location=MEDIA_PATH)
    cart = {}
    item_sum = 0

    with cart_file.open("shopping_info.json", "r") as f:
        try:
            cart = json.load(f)
        except:
            cart = {}
    
    context_data["cart"] = []
    for key in cart["cart"]:
        item = cart["cart"][key]
        db_item = ShopItem.objects.filter(image=item["name"])[0]

        item_sum += float(db_item.price) * float(item["amount"])
        context_data["cart"].append(generateItemInfo(db_item))

    context_data["total"] = round(item_sum, 2)
    recordUrl(redirect("shop-checkout").url)
    return render(request, 'shopcenter/checkout.html', context_data)

def shopPetSupplies(request):
    recordUrl(redirect("shop-ptsp").url)
    return shoppingPage(request, "pet supplies", "shopping")

def shopToys(request):
    recordUrl(redirect("shop-toys").url)
    return shoppingPage(request, "toys", "shopping")

def shopSports(request):
    recordUrl(redirect("shop-spts").url)
    return shoppingPage(request, "sports", "shopping")

def shopElectronics(request):
    recordUrl(redirect("shop-elec").url)
    return shoppingPage(request, "electronics", "shopping")

def shopFurniture(request):
    recordUrl(redirect("shop-furn").url)
    return shoppingPage(request, "furniture", "shopping")

def shopOutDoors(request):
    recordUrl(redirect("shop-otdr").url)
    return shoppingPage(request, "outdoors", "shopping")

def shopSearch(request):
    items = ShopItem.objects.all()
    cart = readShoppingJson()
    context_data = {
        _TITLE_KEY: "Search",
        "cart_size": len(cart["cart"]),
        "selection": [] 
    }
    print("searching")
    for item in items:
        if cart[_SEARCH_STR].lower() in item.name.lower():
            context_data["selection"].append(generateItemInfo(item))

    recordUrl(redirect('shop-search').url)
    return render(request, "shopcenter/shopping.html", context_data)

def sources(request):
    context_data = {
        _TITLE_KEY: "Sources",
        "cart_size": getNumOfItemsInCart(),
        "sources": []
    }

    for item in ShopItem.objects.all():
        context_data["sources"].append(generateItemInfo(item))

    return render(request, "shopcenter/sources.html", context_data)
