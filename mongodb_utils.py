import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['academicworld']

print(myclient.list_database_names())


def pub_cnt(input):
	pipeline = [{'$unwind': "$keywords"},
				{'$match': {'year': input}},
				{'$group': {'_id': '$keywords.name', 'pub_cnt': {'$sum': 1}}},
				{'$sort': {'pub_cnt': -1}},
				{'$limit': 10},
				{'$project'}
				]


	result = mydb.publications.aggregate(pipeline)
	return result

def pub_keyword(query_string):
	pipeline = [{'$unwind': "$keywords"},
				{'$match': {'keywords.name': {'$regex': query_string}}},

				{'$addFields': {"score": {'$multiply': ["$numCitations", "$keywords.score"]}}},
				{'$sort': {'score': -1}},
				{'$limit': 100},
				{'$project': {"title": 1, "year": 1, "numCitations": 1,"score":1, "_id": 0}}
				]

	result = mydb.publications.aggregate(pipeline)
	return [r for r in result]

if __name__ == '__main__':
	#print (pub_cnt())
	print(
		pub_keyword('data mining')
	)

	
