from bson import ObjectId

def objectIdToStr(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj