
python -m venv venv

.\venv\Scripts\activate


pip install pymongo


# PyMongo

PyMongo is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python. This documentation attempts to explain everything you need to know to use PyMongo[.](https://pymongo.readthedocs.io/en/stable/examples/index.html)


##  List Databases present in MongoDB
[.](https://pythonexamples.org/python-mongodb-list-databases/)
```
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
for db in myclient.list_databases():
    print(db)
```

## Get list of MongoDB Collections
```
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#use database "organisation"
mydb = myclient['organisation']

print("List of collections\n--------------------")
#list the collections
for coll in mydb.list_collection_names():
    print(coll)

```

## Create Database
Note: Database is actually created when there is content in the database. So, only when there is atleast one document inside the database, you could see that the database is created when you run list_databases() function. In the following example, we have created the database, inserted a document and then listed the databases.
```
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#use database named "organisation"
mydb = myclient["organisation"]
```


## Create Collection
```
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#use database named "organisation"
mydb = myclient["organisation"]
#new collection named "testers"
mycol = mydb["testers"]
```

## Delete Collection

```
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["organisation"]
#get collection named "developers"
mycol = mydb["developers"]
#delete or drop collection
mycol.drop()
```


## Update
Update One
```
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

myquery = { "address": "Valley 345" }
newvalues = { "$set": { "address": "Canyon 123" } }

mycol.update_one(myquery, newvalues)

#print "customers" after the update:
for x in mycol.find():
  print(x) 
```

[.](https://kb.objectrocket.com/mongo-db/how-to-update-a-mongodb-document-in-python-356)
```
doc = col.find_one_and_update(
    {"_id" : ObjectId("5cfbb46d6fb0f3245fd8fd34")},
    {"$set":
        {"some field": "OBJECTROCKET ROCKS!!"}
    },upsert=True
)
```

Update Many[.](https://www.w3schools.com/python/python_mongodb_update.asp)
```
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

myquery = { "address": { "$regex": "^S" } }
newvalues = { "$set": { "name": "Minnie" } }

x = mycol.update_many(myquery, newvalues)

print(x.modified_count, "documents updated.") 
```

### How to update an entire document in a collection
To replace the whole document, you don't use $set, but just provide the new doc to the update call[:](https://stackoverflow.com/questions/24714022/mongodb-how-to-update-an-entire-document-in-a-collection)
```
db.test.update({"_id": ObjectId("53b986e2fe000000019a5a13")}, {
  "_id" : ObjectId("53b986e2fe000000019a5a13"),
  "name" : "Joe",
  "birthDate" : "1980-12-11",
  "publications" : [
    { "title" : "bye bye", "description" : "Blah blah" },
    { "title" : "title 2", "description" : "description 2" },
    { "title" : "title 3", "description" : "description 3" }
  ]
})
```

However, with the current 3.0 driver, it would be best to use replaceOne instead:
```


To replace the whole document, you don't use $set, but just provide the new doc to the update call:

db.test.update({"_id": ObjectId("53b986e2fe000000019a5a13")}, {
  "_id" : ObjectId("53b986e2fe000000019a5a13"),
  "name" : "Joe",
  "birthDate" : "1980-12-11",
  "publications" : [
    { "title" : "bye bye", "description" : "Blah blah" },
    { "title" : "title 2", "description" : "description 2" },
    { "title" : "title 3", "description" : "description 3" }
  ]
})

However, with the current 3.0 driver, it would be best to use replaceOne instead:
```
db.test.replaceOne({"_id": ObjectId("53b986e2fe000000019a5a13")}, {
  "name" : "Joe",
  "birthDate" : "1980-12-11",
  "publications" : [
    { "title" : "bye bye", "description" : "Blah blah" },
    { "title" : "title 2", "description" : "description 2" },
    { "title" : "title 3", "description" : "description 3" }
  ]
})

```