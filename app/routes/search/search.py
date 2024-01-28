from app import app, mongo
from app.models.Part import Part
from app.utils.levenshtein_dist import find_minimum_levenshtein_distance
from app.utils.objectIdToStr import objectIdToStr
from flask import jsonify

@app.route('/search/<key>/<limit>', methods=['GET'])
def search(key, limit):
    key = str(key)
    limit = int(limit)
    
    parts = mongo.db.parts.find()
    tab = []
    for part in parts:
        part['_id'] = objectIdToStr(part['_id'])
        tab.append(part)

    ret = []

    tmp1 = ["category", "description", "name", "price", "quantity", "serial_number"]
    tmp2 = ["bookcase", "column", "cuvette", "room", "row", "shelf"]
    for part in tab:
        tmp_ret = []
        for i in tmp1:
            tmp_ret.append(str(part[i]))
        for i in tmp2:
            tmp_ret.append(str(part["location"][i]))

        ret.append((find_minimum_levenshtein_distance(key, tmp_ret), part["_id"]))
    
    return jsonify(sorted(ret, key=lambda x: x[0])[:limit])