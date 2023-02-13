

# State Report
select State, count(_id)  from articledata group by State;

```
// Requires official MongoShell 3.6+
use articledata;
db.getCollection("articledata").aggregate(
    [
        { 
            "$group" : { 
                "_id" : { 
                    "State" : "$State"
                }, 
                "COUNT(_id)" : { 
                    "$sum" : NumberInt(1)
                }
            }
        }, 
        { 
            "$project" : { 
                "State" : "$_id.State", 
                "COUNT(_id)" : "$COUNT(_id)", 
                "_id" : NumberInt(0)
            }
        }
    ], 
    { 
        "allowDiskUse" : true
    }
);
```


# List of PMID base on State
select PMID  from articledata where State = -1

```
// Requires official MongoShell 3.6+
use articledata;
db.getCollection("articledata").find(
    { 
        "State" : NumberLong(-1)
    }, 
    { 
        "PMID" : "$PMID", 
        "_id" : NumberInt(0)
    }
);

```

