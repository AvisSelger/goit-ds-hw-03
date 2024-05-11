from pymongo import MongoClient
from bson.objectid import ObjectId

def get_database():
    client = MongoClient('mongodb://localhost:27017/')
    return client['catdb']

# CRUD Operation

def create_cat(name, age, features):
    db = get_database()
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return db.cats.insert_one(cat).inserted_id

def get_all_cats():
    db = get_database()
    return list(db.cats.find())

def get_cat_by_name(name):
    db = get_database()
    return db.cats.find_one({"name": name})

def update_cat_age(name, new_age):
    db = get_database()
    result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    return result.modified_count

def add_feature_to_cat(name, feature):
    db = get_database()
    result = db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
    return result.modified_count

def delete_cat_by_name(name):
    db = get_database()
    result = db.cats.delete_one({"name": name})
    return result.deleted_count

def delete_all_cats():
    db = get_database()
    result = db.cats.delete_many({})
    return result.deleted_count

if __name__ == "__main__":
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("murchik", 5, ["ласкавий", "спить день"])
    print("All cats:", get_all_cats())
    print("Cat by name:", get_cat_by_name("barsik"))
    update_cat_age("barsik", 4)
    add_feature_to_cat("murchik", "грається з м'ячиком")
    delete_cat_by_name("murchik")
    print("All cats after delete:", get_all_cats())

    delete_all_cats()
