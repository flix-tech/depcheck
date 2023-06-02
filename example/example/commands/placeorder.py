from example import customer, booking
from example.customer import account
from example.products import prices
from example.payments import payment


def place_order():
    customer_id = customer.get_id()
    balance = account.get_balance(customer_id)
    product = booking.get_product()
    price = prices.get_price_for(product, customer_id)

    if balance < price:
        missing_money = price - balance
        print(
            f"-> Customer {customer_id} cannot afford {product}, he is missing ${missing_money}"
        )
        return

    payment.register_payment(customer_id, balance, price)


place_order() if __name__ == "__main__" else None
