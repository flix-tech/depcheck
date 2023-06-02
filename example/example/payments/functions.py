from example.customer.account.account import update_balance


def register_payment(customer_id: str, balance: float, price: float) -> None:
    new_balance = balance - price
    print(
        f"-> Customer {customer_id} pays ${price} and now has only ${new_balance} left"
    )
    update_balance(customer_id, new_balance)
