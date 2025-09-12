from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Order
from django.http import FileResponse, Http404
from django.conf import settings
from pathlib import Path


def home(request):
    products = Product.objects.all()
    promos = Product.objects.filter(is_promo=True)[:6]
    coffret_products = Product.objects.filter(category='coffret')[:6]
    return render(request, "home.html", {
        "products": products, 
        "promos": promos, 
        "coffret_products": coffret_products,
        "brand": "al-anaqawatch"
    })


def promo_page(request):
    promos = Product.objects.filter(is_promo=True)
    return render(request, "promo.html", {
        "promos": promos,
        "brand": "al-anaqawatch"
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product_detail.html", {"product": product, "brand": "al-anaqawatch"})


def cart_view(request):
    cart = request.session.get("cart", {"items": {}})
    items = cart.get("items", {})
    products = Product.objects.filter(id__in=items.keys()) if items else []
    enriched = []
    total = 0
    for p in products:
        qty = int(items.get(str(p.id), 0))
        line_total = qty * float(p.price)
        total += line_total
        enriched.append({"product": p, "qty": qty, "line_total": line_total})
    return render(request, "cart.html", {"lines": enriched, "total": total, "brand": "al-anaqawatch"})


def cart_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {"items": {}})
    items = cart.get("items", {})
    items[str(product.id)] = int(items.get(str(product.id), 0)) + int(request.POST.get("qty", 1))
    cart["items"] = items
    request.session["cart"] = cart
    return redirect("cart_view")


def cart_remove(request, product_id: int):
    cart = request.session.get("cart", {"items": {}})
    items = cart.get("items", {})
    items.pop(str(product_id), None)
    cart["items"] = items
    request.session["cart"] = cart
    return redirect("cart_view")


def cart_clear(request):
    request.session["cart"] = {"items": {}}
    return redirect("cart_view")


def category_list(request, category_slug: str):
    category_map = {
        "coffret": Product.CATEGORY_COFFRET,
        "boite_simple": Product.CATEGORY_BOITE_SIMPLE,
        "wallets": Product.CATEGORY_WALLETS,
        "packs": Product.CATEGORY_PACKS,
    }
    category = category_map.get(category_slug)
    if not category:
        return redirect("home")
    items = Product.objects.filter(category=category)
    return render(request, "category.html", {"items": items, "category_slug": category_slug, "brand": "al-anaqawatch"})


def order_create(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        address = request.POST.get("address", "").strip()
        quantity = int(request.POST.get("quantity", 1) or 1)
        notes = request.POST.get("notes", "").strip()

        if not customer_name or not phone_number or not address:
            context = {
                "product": product,
                "brand": "al-anaqawatch",
                "error": "Merci de remplir tous les champs obligatoires.",
                "form": {
                    "customer_name": customer_name,
                    "phone_number": phone_number,
                    "address": address,
                    "quantity": quantity,
                    "notes": notes,
                },
            }
            return render(request, "order_form.html", context)

        order = Order.objects.create(
            product=product,
            customer_name=customer_name,
            phone_number=phone_number,
            address=address,
            quantity=max(1, quantity),
            notes=notes,
        )
        return redirect(reverse("order_success", args=[order.id]))

    return render(request, "order_form.html", {"product": product, "brand": "al-anaqawatch"})


def order_success(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    message = (
        f"Bonjour, je viens de passer une commande sur al-anaqawatch.%0A"
        f"Produit: {order.product.name}%0AQuantité: {order.quantity}%0A"
        f"Nom: {order.customer_name}%0ATéléphone: {order.phone_number}%0A"
        f"Adresse: {order.address}"
    )
    whatsapp_link = f"https://wa.me/212668389257?text={message}"
    return render(
        request,
        "order_success.html",
        {"order": order, "brand": "al-anaqawatch", "whatsapp_link": whatsapp_link},
    )


def serve_media(request, path: str):
    base = Path(settings.MEDIA_ROOT)
    file_path = (base / path).resolve()
    try:
        file_path.relative_to(base)
    except Exception:
        raise Http404()
    if not file_path.exists() or not file_path.is_file():
        raise Http404()
    return FileResponse(open(file_path, 'rb'))
