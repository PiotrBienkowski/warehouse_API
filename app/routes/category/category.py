from app import app, mongo
from app.utils.objectIdToStr import objectIdToStr
from app.models.Category import Category
from bson import ObjectId
from flask import request, jsonify

# ----- CREATE -----
@app.route('/categories', methods=['POST'])
def add_category():
    try:
        data = request.json
        Category.validate(data)
        new_category = Category(**data)
        mongo.db.categories.insert_one(new_category.to_dict())
        return jsonify({'msg': 'Category added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# ----- READ -----
@app.route('/categories', methods=['GET'])
def show_categories():
    categories = mongo.db.categories.find()
    categories_list = []
    for category in categories:
        category['_id'] = objectIdToStr(category['_id'])
        if 'parent_id' in category and category['parent_id']:
            category['parent_id'] = objectIdToStr(category['parent_id'])
        categories_list.append(category)
    return jsonify(categories_list), 200

# ----- UPDATE -----
@app.route('/categories/<id>', methods=['PUT'])
def update_category(id):
    try:
        object_id = ObjectId(id)
    except:
        return jsonify({'error': 'Invalid ObjectId'}), 400

    data = request.json
    try:
        Category.validate(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    result = mongo.db.categories.update_one({'_id': object_id}, {"$set": data})
    if result.matched_count:
        return jsonify({'msg': 'Category updated successfully'}), 200
    else:
        return jsonify({'error': 'Category not found'}), 404
    
# ----- DELETE -----
@app.route('/categories/<id>', methods=['DELETE'])
def delete_category(id):
    try:
        object_id = ObjectId(id)
    except:
        return jsonify({'error': 'Invalid ObjectId'}), 400

    result = mongo.db.categories.delete_one({'_id': object_id})
    if result.deleted_count:
        return jsonify({'msg': 'Category deleted successfully'}), 200
    else:
        return jsonify({'error': 'Category not found'}), 404