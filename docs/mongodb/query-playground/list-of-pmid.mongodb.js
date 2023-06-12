/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('articledata');
db.getCollection("articledata").find(
    { 
        "State" : NumberLong(1)
    }, 
    { 
        "PMID" : "$PMID", 
        "_id" : NumberInt(0)
    }
).limit(10);