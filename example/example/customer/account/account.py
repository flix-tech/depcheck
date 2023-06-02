from random import randrange


def get_balance(customer_id: str) -> float:
    cents = randrange(0, 99)
    dollars = randrange(0, 2000)
    balance = float(f"{dollars}.{cents}")
    print(f"-> Customer {customer_id} has a balance of ${balance}")
    return balance


def update_balance(customer_id: str, new_balance: float) -> None:
    print(f"-> Balance updated for {customer_id} to {new_balance}")


def get_voucher(customer_id: str) -> float:
    cents = randrange(0, 99)
    dollars = randrange(0, 100)
    voucher = float(f"{dollars}.{cents}")
    print(f"-> Customer {customer_id} has a voucher worth {voucher}")
    return voucher
