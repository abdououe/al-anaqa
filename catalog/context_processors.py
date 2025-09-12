from .models import Product


def cart(request):
    session_cart = request.session.get("cart", {"items": {}})
    items = session_cart.get("items", {})
    count = sum(items.values()) if isinstance(items, dict) else 0
    total = 0
    if items:
        # keys may be strings; normalize to strings for lookup
        product_ids = [int(k) for k in items.keys()]
        for p in Product.objects.filter(id__in=product_ids):
            qty = int(items.get(str(p.id), 0))
            total += float(p.price) * qty
    return {"cart": {"count": count, "total": total}}






