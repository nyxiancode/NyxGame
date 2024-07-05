from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']  # Replace 'your_database' with your actual database name
collection = db['goods']  # Collection name for your data

# Example function to insert or update data
def save_data(us_name, name, money, anm, ad_anm):
    # Example data structure, adjust as per your requirements
    data = {
        'us_name': us_name,
        'name': name,
        'money': money,
        'anm': anm,
        'ad_anm': ad_anm
    }
    collection.update_one({'us_name': us_name}, {'$set': data}, upsert=True)

# Example function to retrieve data
def get_data(us_name):
    data = collection.find_one({'us_name': us_name})
    return data

# Example function to delete data
def delete_data(us_name):
    collection.delete_one({'us_name': us_name})

# Additional functions as needed...

if __name__ == '__main__':
    # Test your functions here if needed
    pass
