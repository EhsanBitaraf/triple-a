

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


# Get List of Keywords

```
db.getCollection("articledata").aggregate([
  { $unwind: "$Keywords" },
  { $group: { _id: "$Keywords.Text", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```


# Get Article List With Specific Keyword

```
db.getCollection("articledata").find({$or:[{"Keywords.Text": "biobank"},{"Keywords.Text": "bank"}]}, {"Title": 1 , "PMID" : 1})
```

# Get List of Topics

```
db.getCollection("articledata").aggregate([
  { $unwind: "$Topics" },
  { $group: { _id: "$Topics", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

# Get Article List With Specific Topic


```
db.getCollection("articledata").find({$or:[{"Topics": "biobank"},{"Topics": "Bank"}]}, {"Title": 1 , "PMID" : 1})
```

or like type:

```
db.getCollection("articledata").find(
{$or:[
    {"Topics": /biobank/ },
    {"Topics": /Biobank/},
    {"Topics": /Bio-bank/}
    ]
    }, {"Title": 1 , "PMID" : 1})
```
