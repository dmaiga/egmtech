from decimal import Decimal
from catalog.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        # On utilise le prix promo si disponible
        price = product.get_promo_price() if hasattr(product, 'get_promo_price') else product.price
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(price)}
        
        if override_quantity:
            # Remplace la quantité (utile si on change la valeur dans le panier)
            self.cart[product_id]['quantity'] = quantity
        else:
            # Ajoute à la quantité existante (utile depuis la fiche produit)
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()