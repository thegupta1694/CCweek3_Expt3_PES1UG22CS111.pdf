from products import dao
from functools import lru_cache


class Product:
    __slots__ = ['id', 'name', 'description', 'cost', 'qty']

    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @classmethod
    def load(cls, data: dict):
        """Class method to create a Product object."""
        return cls(*[data[key] for key in cls.__slots__])


def list_products() -> iter:
    """Efficiently list all products with lazy evaluation."""
    return (Product.load(product) for product in dao.list_products())


@lru_cache(maxsize=100)
def get_product(product_id: int) -> Product | None:
    """Retrieve product details by ID with caching."""
    product_data = dao.get_product(product_id)
    return Product.load(product_data) if product_data else None


def add_product(product: dict):
    """Add a new product using the DAO."""
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """Update the quantity of a product."""
    if qty < 0:
        raise ValueError("Quantity cannot be negative")
    rows_updated = dao.update_qty(product_id, qty)  # Update returns affected rows
    if rows_updated == 0:
        raise ValueError("Product does not exist")
