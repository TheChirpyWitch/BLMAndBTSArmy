import csv
import pymongo


if __name__ == "__main__":

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["bts"]
	mycol = mydb["tweets"]

	d = {} #{no. of followers: no. of nodes}

	col2 = mydb["users"]
	"""
	for document in mycol.find():
		user = document["user"]
		user_id = document["user"]["id"]
		if mydb.col2.count_documents({'id': user_id}) == 0:
			x = col2.insert_one(user)


	"""
	for document in col2.find():
		degree = document["followers_count"]


		if degree not in d:
			d[degree] = 1
		else:
			d[degree] += 1

	#print(d)
	with open('followers_powerlaw.csv', 'w') as f:
		for key in d.keys():
			f.write("%s,%s\n"%(key,d[key]))

