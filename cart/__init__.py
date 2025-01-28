import json
from typing import List, Optional
from products import Product, get_product
from cart import dao


class Cart:
    """
    Represents a shopping cart with user-specific details.
    """
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        """
        Creates a Cart instance from a dictionary.
        """
        return Cart(
            id=data["id"],
            username=data["username"],
            contents=[get_product(product_id) for product_id in data["contents"]],
            cost=data["cost"]
        )


def get_cart(username: str) -> List[Product]:
    """
    Fetches the cart contents for a given username.

    Args:
        username (str): The username for whom the cart is fetched.

    Returns:
        List[Product]: List of products in the user's cart.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail["contents"])
            items.extend(contents)
        except (json.JSONDecodeError, KeyError):
            continue

    return [get_product(product_id) for product_id in items]


def add_to_cart(username: str, product_id: int) -> None:
    """
    Adds a product to the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The ID of the product to add.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Removes a product from the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The ID of the product to remove.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """
    Deletes the user's entire cart.

    Args:
        username (str): The username of the user.
    """
    dao.delete_cart(username)
