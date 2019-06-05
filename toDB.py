import json
import pymongo
import sys, getopt
import os

def getPara(argv = sys.argv[1:]):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"i:",["ifile="])
	except getopt.GetoptError:
		print ('toDB.py -i <inputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--ifile"):
			inputfile = arg
	print ('input file : ',inputfile)
	return inputfile



def getAllData(rootdir):
	data = {}
	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if name.endswith('.json'):
				with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
					tmp = json.load(f)
					data.update(tmp)
	print ('data size : ', len(data))
	return data




if __name__ == "__main__":

	mongo_uri = 'mongodb://mongodb:mongodb@166.111.110.94:27017/'
	client = pymongo.MongoClient(
		mongo_uri,
		unicode_decode_error_handler='ignore'
	)
	db = client.qschou
	collection = db.end_project


	inputfile = getPara()
	data = getAllData(inputfile)

	for uid in data:
		try:
			toJson = {uid: data[uid], '_id': uid}
			if collection.find_one({'_id': uid}):
				collection.update_one({'_id': uid}, {'$set': toJson})
			else:
				collection.insert_one(toJson)
		except:
			print (uid)
