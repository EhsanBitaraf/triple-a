
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