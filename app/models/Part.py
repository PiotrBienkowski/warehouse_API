from app.models.Category import Category

class Part:
    def __init__(self, serial_number, name, description, category, quantity, price, location):
        self.serial_number = serial_number
        self.name = name
        self.description = description
        self.category = category
        self.quantity = quantity
        self.price = price
        self.location = location

    def to_dict(self):
        return {
            "serial_number": self.serial_number,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
            "location": self.location
        }

    @staticmethod
    def validate(data, mongo):
        if not isinstance(data.get('serial_number'), str):
            raise ValueError("Serial number must be a string")
        if not isinstance(data.get('name'), str):
            raise ValueError("Name must be a string")
        if not isinstance(data.get('description'), str):
            raise ValueError("Description must be a string")
        if not isinstance(data.get('category'), str):
            raise ValueError("Category must be a string")
        if not isinstance(data.get('quantity'), int) or data.get('quantity') < 0:
            raise ValueError("Quantity must be a non-negative integer")
        if not isinstance(data.get('price'), (int, float)) or data.get('price') < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(data.get('location'), dict):
            raise ValueError("Location must be a dictionary")
        if 'category' in data:
            if not Category.exists(data['category'], mongo):
                raise ValueError("Category does not exist")
        return True
