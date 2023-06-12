/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('articledata');
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