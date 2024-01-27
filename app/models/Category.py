from bson import ObjectId

class Category:
    def __init__(self, name, parent_id=None):
        self.name = name
        self.parent_id = ObjectId(parent_id) if parent_id else None

    def to_dict(self):
        return {
            "name": self.name,
            "parent_id": str(self.parent_id) if self.parent_id else None
        }

    @staticmethod
    def validate(data):
        if not isinstance(data.get('name'), str):
            raise ValueError("Name must be a string")
        if data.get('parent_id') and not ObjectId.is_valid(data.get('parent_id')):
            raise ValueError("Parent ID must be a valid ObjectId")
        return True