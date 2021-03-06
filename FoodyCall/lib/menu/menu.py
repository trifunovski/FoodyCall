from flask import Blueprint
from flask import json
from flask import jsonify
from flask import make_response
from flask import request
from pymongo import MongoClient
import csv
import sys
from datetime import datetime, time
import pytz


# Create Blueprint
menu = Blueprint('menu', __name__, template_folder='templates')

# Initialize connection with mongo :^)
# This connects to the default port and host, localhost and 27017.
client = MongoClient()
db = client.menudb
menu_items = db.menu_items

menu_to_serve = "none"

# Get the time and choose which menu to load, then get the collection of items
#now = datetime.now()
#fmt = "%Y-%m-%d %H:%M:%S %Z%z"
now = datetime.now(pytz.timezone('US/Eastern'))
print(now)
if (time(21,30) <= now.time() <= time(23,59)) or (time(00,00) <= now.time() < time(01,00)):
	menu_to_serve = "latenight"
elif (time(11,00) <= now.time() < time(14,00)) or (time(17,30) <= now.time() < time(21,00)) :
	menu_to_serve = "summies"
else:
	print "Invalid time: defaulting to summies for dev purposes"
	menu_to_serve = "summies"

order_history = db.order_history

@menu.route('/<number>')
def popular(number=9999999999):

		filter = {}
		if menu_to_serve == "summies":
			filter = {"menu": "s"}
		elif menu_to_serve == "latenight":
			filter = {"menu": "ln"}
		else:
			filter = {}

		menulist = []
		for item in menu_items.find(filter):
			menulist.append({"_id": str(item['_id']),
				"description": item['description'],
				"filter": item['filter'], "item": item['item'],
				"menu": item['menu'], "price": item['price'], "rater_count": item['rater_count'],
				"rating_avg": item['rating_avg'], "side": item['side'], "count": 0})

			for order in order_history.find():
				if str(number) == str(order['user']):
					if order['item_id'] == item['_id']:
						item['count'] = item['count'] + 1
		return json.dumps(menulist)


