  "retweets_count" column in "originalTweet_841_4columns_v2.csv" indicates number of retweets done by unique user's followers
- use countif function in excel to get count of each node in column named "user_id" with range argument from column named "source_user_id" in "retweet_12349_5columns_org.csv" file.

  "follower_count" column in "originalTweet_841_4columns_v2.csv" indicates count of each unique user's followers
- set up followers in mongo by importing file "follower_data.json", example mongo command: mongoimport --db dbName --collection collectionName --file fileName.json
- get count of followers in a separate collection, example mongo command: db.followerData.aggregate([{$project:{id:1, item:1, numberOfFollowers:{$cond:{if:{$isArray:"$follower_list"},then:{$size:"$follower_list"}, else:"NA"}}}},{$out:"followerCount"}])
  where "followerData" is collection with "follower_data.json" data, "followerCount" is new collection output.
- export "followerCount" collection to get count of followers, example mongo command: mongoexport --db dbName --collection collectionName --type=json  --out "follower_count.json" 

- convert exported "follower_count.json" to csv file

- add follower count in a column named "follower_count" to each unique "user_id" node in "originalTweet_841_4columns_v2.csv" file using vlookup function in excel.

- final "emmbeddedness" column in "originalTweet_841_4columns_v2.csv" file is calculated by following division: "retweets_count"/"follower_count".
