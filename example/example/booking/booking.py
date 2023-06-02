from random import choice

from example.products import get_inventory


def get_product():
    options = get_inventory()
    product = choice(options)
    print(f"-> He wants to buy {product}")
    return product
