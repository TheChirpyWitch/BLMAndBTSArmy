import csv
import pymongo


if __name__ == "__main__":

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["bts"]
	mycol = mydb["tweets"]

	d = {} #{no. of followers: no. of nodes}

	for document in mycol.find():
		#print(type(document))
		user = document["user"]

		#followers_count = get_followers_count(target)
		#mydict = { "id": target, "followers_count": followers_count }

		#x = mycol.insert_one(mydict)
		#print(user["id"])
		degree = user["followers_count"]


		if degree not in d:
			d[degree] = 1
		else:
			d[degree] += 1

	#print(d)
	with open('followers_powerlaw.csv', 'w') as f:
		for key in d.keys():
			f.write("%s,%s\n"%(key,d[key]))

