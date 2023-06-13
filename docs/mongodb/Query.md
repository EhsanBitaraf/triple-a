

# State Report
```sql
select State, count(_id)  from articledata group by State;
```


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

```sql
select PMID  from articledata where State = -1
```

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

# Get Article Base on PMID

```sql
select *  from articledata where PMID = '37301943'
```

```json
use articledata;
db.getCollection("articledata").find(
    { 
        "PMID" : "37301943"
    }
);

```

# Change ReferenceCrawlerDeep

```sql
Update articledata SET ReferenceCrawlerDeep = 0 where ReferenceCrawlerDeep = 1
```
* Not work in Studio3d


```
use articledata;
db.articledata.updateMany(
  { ReferenceCrawlerDeep: 1 },
  { $set: { ReferenceCrawlerDeep: 0 } }
);

```
