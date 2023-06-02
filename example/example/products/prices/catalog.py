from example.customer.account.account import get_voucher


def get_price_for(product: str, customer_id: str) -> float:
    price_dict = {
        "an apple": 3.66,
        "an iphone": 899.99,
        "a whiteboard": 120,
        "a helicopter": 5000000,
    }

    if product not in price_dict:
        raise Exception("The product does not have a price!")
    print(f"-> {product} costs ${price_dict[product]}")
    # Let's add some horrible ideas to make spaghetti code: get if there is a voucher here
    voucher = get_voucher(customer_id)
    updated_price = price_dict[product] - voucher
    print(f"-> with voucher, {product} costs ${updated_price}")

    return updated_price
