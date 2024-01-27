from flask import request, jsonify
from app import app, mongo
from app.models.Category import Category

@app.route('/add_category', methods=['POST'])
def add_category():
    try:
        data = request.json
        Category.validate(data)
        new_category = Category(**data)
        mongo.db.categories.insert_one(new_category.to_dict())
        return jsonify({'msg': 'Category added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    