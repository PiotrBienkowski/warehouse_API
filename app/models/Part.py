from app.models.Category import Category
from bson import ObjectId
from queue import Queue

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
            if Category.is_base(data['category'], mongo):
                raise ValueError("Category cannot be a basic category")
            
        location_keys = ["room", "bookcase", "shelf", "cuvette", "column", "row"]
        location_data = data.get('location')

        if not isinstance(location_data, dict):
            raise ValueError("Location must be a dictionary")

        if set(location_keys) != set(location_data.keys()):
            raise ValueError("Location must contain all and only these keys: " + ", ".join(location_keys))

        serial_number = data.get('serial_number')
        if not isinstance(serial_number, str):
            raise ValueError("Serial number must be a string")

        existing_part = mongo.db.parts.find_one({"serial_number": serial_number})
        if existing_part:
            raise ValueError("Serial number already exists in the database")

        return True

    @classmethod
    def category_has_parts(cls, category_id, mongo, case=False):
        try:
            object_id = ObjectId(category_id)
            if case:
                category_id = object_id
        except:
            raise ValueError("Invalid category ID")

        return mongo.db.parts.find_one({"category": category_id}) is not None
    
    @classmethod
    def has_parts_in_subtree(cls, root_category_id, mongo):
        # I use BFS (DFS would be ok too) to check if my descendants have parts
        visited = set()
        q = Queue()
        q.put(root_category_id)
        visited.add(root_category_id)

        while not q.empty():
            current_id = q.get()

            if cls.category_has_parts(str(current_id), mongo):
                return True

            child_categories = mongo.db.categories.find({'parent_id': current_id})

            for category in child_categories:
                category_id = category['_id']
                if category_id not in visited:
                    category_id = ObjectId(category_id)
                    q.put(category_id)
                    visited.add(category_id)

        return False