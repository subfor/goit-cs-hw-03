import os

from pymongo import MongoClient, errors


class MongoSession:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def __enter__(self):
        try:
            mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
            mongo_pass = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
            mongo_host = os.getenv("MONGO_HOST", "localhost")
            mongo_port = int(os.getenv("MONGO_PORT", 27017))  # дефолт, якщо не задано
            mongo_db = os.getenv("MONGO_DB", "cats_db")  # дефолт, якщо не задано
            mongo_collection = os.getenv(
                "MONGO_COLLECTION", "cats"
            )  # дефолт, якщо не задано

            uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/"
            self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")  # Перевірка з'єднання
            self.db = self.client[mongo_db]
            self.collection = self.db[mongo_collection]
            print("З'єднання з MongoDB встановлено!")
            return self
        except errors.ConnectionFailure as e:
            print(f"Помилка підключення до MongoDB: {e}")
            raise
        except Exception as e:
            print(f"Інша помилка: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            print("З'єднання з MongoDB закрито.")


#  CRUD функції
def insert_cat(collection, name, age, features):
    doc = {"name": name, "age": age, "features": features}
    try:
        result = collection.insert_one(doc)
        print(f"Кота {name} додано з _id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print(f"Помилка вставки: {e}")


def show_all_cats(collection):
    try:
        print("\nВсі коти:")
        for cat in collection.find():
            print(cat)
    except errors.PyMongoError as e:
        print(f"Помилка читання: {e}")


def find_cat_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print("\nЗнайдено кота:")
            print(cat)
        else:
            print(f"\nКота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка пошуку: {e}")


def update_cat_age(collection, name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"\nВік кота {name} оновлено до {new_age}")
        else:
            print(f"\nКота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка оновлення: {e}")


def add_feature(collection, name, new_feature):
    try:
        result = collection.update_one(
            {"name": name}, {"$addToSet": {"features": new_feature}}
        )
        if result.matched_count:
            print(f"\nДодано характеристику '{new_feature}' коту {name}")
        else:
            print(f"\nКота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка оновлення features: {e}")


def delete_cat_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"\nКота {name} видалено.")
        else:
            print(f"\nКота з ім'ям {name} не знайдено.")
    except errors.PyMongoError as e:
        print(f"Помилка видалення: {e}")


def delete_all_cats(collection):
    try:
        result = collection.delete_many({})
        print(f"\nВидалено всіх котів ({result.deleted_count}) з колекції.")
    except errors.PyMongoError as e:
        print(f"Помилка очищення колекції: {e}")


if __name__ == "__main__":
    with MongoSession() as mongo:
        insert_cat(
            mongo.collection,
            "barsik",
            3,
            ["ходить в капці", "дає себе гладити", "рудий"],
        )
        insert_cat(
            mongo.collection, "murka", 4, ["мурчить", "сіра", "лягає на клавіатуру"]
        )

        show_all_cats(mongo.collection)
        find_cat_by_name(mongo.collection, "barsik")
        update_cat_age(mongo.collection, "barsik", 5)
        find_cat_by_name(mongo.collection, "barsik")
        add_feature(mongo.collection, "barsik", "любить їсти")
        find_cat_by_name(mongo.collection, "barsik")
        delete_cat_by_name(mongo.collection, "murka")
        delete_all_cats(mongo.collection)
