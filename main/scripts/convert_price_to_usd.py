from main.models import Product


def run():
    products = Product.objects.all()

    for product in products:
        product.save()