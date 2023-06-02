import uuid


def get_id() -> str:
    customer_id = str(uuid.uuid4())
    print(f"-> Setting customer id to {customer_id}")
    return customer_id
