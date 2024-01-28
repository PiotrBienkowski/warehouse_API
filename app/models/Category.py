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
    
    @classmethod
    def is_ancestor(cls, category_id, potential_ancestor_id, mongo):
        # this method prevents making a cycle in the tree (especially with UPDATE operation), prevents the son of a vertex from being an ancestor
        if category_id == potential_ancestor_id:
            return True

        category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
        if not category or 'parent_id' not in category or not category['parent_id']:
            return False

        return cls.is_ancestor(category['parent_id'], potential_ancestor_id, mongo)

    @staticmethod
    def validate(data, mongo):
        if not isinstance(data.get('name'), str):
            raise ValueError("Name must be a string")
        parent_id = data.get('parent_id')
        if parent_id:
            if not ObjectId.is_valid(parent_id):
                raise ValueError("Parent ID must be a valid ObjectId")

            if not Category.exists(parent_id, mongo):
                raise ValueError("Parent category with the given ID does not exist")

        if '_id' in data:
                if Category.is_ancestor(parent_id, data['_id'], mongo):
                    raise ValueError("A category cannot be its own ancestor")
    
        return True
    
    
    @classmethod
    def exists(cls, category_id, mongo):
        try:
            object_id = ObjectId(category_id)
        except:
            return False

        category = mongo.db.categories.find_one({'_id': object_id})
        return bool(category)
    
    @classmethod
    def is_base(cls, category_id, mongo):
        try:
            object_id = ObjectId(category_id)
        except:
            return False

        category = mongo.db.categories.find_one({'_id': object_id})
        return category is not None and category.get('parent_id') is None