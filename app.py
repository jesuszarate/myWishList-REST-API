#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import render_template

app = Flask(__name__)

def is_float_try(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

lst = [
    {
        'index': 1,
        'name': u'Edge',
        'location': u'Samsung',
        'price': u'700',
        'sale': False,
        'want': u'10',
        'longitude' : -111.111111,
        'latitude' : 000.000000
        },   
    {
        'index': 2,
        'name': u'Cologne',
        'location': u'Hollister',
        'price': u'50',
        'sale': False,
        'want': u'10',
        'longitude' : -111.111111,
        'latitude' : 000.000000
        }
    ]

lst1 = []

users_lists = [
    {
        'uid' : 1,
        'lst' : lst
        },
    {
        'uid' : 2,
        'lst' : lst1
        }
    ]

users = [
    {
        'uid' : 1,
        'userName' : u'Jayjita'
        },
    {
        'uid' : 2,
        'userName' : u'Chucho'
        }
    ]

###
### Ensures that the request contains every field
###
def check_fields(req):
    if not req.json or\
            not 'name' in req.json or\
            not 'location' in req.json or\
            not 'price' in req.json or\
            not 'sale' in req.json or\
            not 'want' in req.json or\
            not 'longitude' in req.json or\
            not 'latitude' in req.json:
        abort(400)

def check_item_fields(req):
    if not req.json or not 'name' in req.json:
        abort(400)

@app.route('/myWishList/api/v1.0/', methods=['GET'])
def get_greeting(name=None):
    return render_template('index.html')
        

# Get item list by user id (not quite)
@app.route('/myWishList/api/v1.0/list/<int:user_id>', methods=['GET'])
def get_list(user_id):
    for l in lst:
        if l['index'] == user_id:
            return jsonify({"usrList" : lst})
    abort(404)

###
### Get the list of users
###
@app.route('/myWishList/api/v1.0/users', methods=['GET'])
def get_one_list():
    return jsonify({"usrList" : users_lists}), 201

###
### Add a new item to a user by their id number 
###
@app.route('/myWishList/api/v1.0/list/<int:user_id>', methods=['POST'])
def create_item(user_id):
    check_item_fields(request)

    tmp_lst = []

    for urs in users_lists:
        if urs['uid'] == user_id:
            tmp_lst = urs['lst']

    ind = 1
    if len(tmp_lst) > 0:
        ind = tmp_lst[-1]['index'] + 1

    if not is_float_try(request.json['longitude']) and\
            not is_float_try(request.json['latitude']) and\
            not is_float_try(request.json['price']):                                 
        abort(404)

    item = {
        'index': ind,
        'name' : request.json['name'],
        'location' : request.json['location'],
        'price' : float(request.json['price']),
        'sale' : request.json['sale'],
        'want' : request.json['want'],
        'longitude' : float(request.json['longitude']),
        'latitude' : float(request.json['latitude']),
        }
    tmp_lst.append(item)
    return jsonify({'item': item}), 201

###
### Might not need this anymore
###
@app.route('/myWishList/api/v1.0/list', methods=['POST'])
def create_item_1():
    check_fields(request)    
    print request
    item = {
        'index': lst[-1]['index'] + 1,
        'name' : request.json['name'],
        'location' : request.json['location'],
        'price' : request.json['price'],
        'sale' : request.json['sale'],
        'want' : request.json['want'],
        'longitude' : request.json['longitude'],
        'latitude' : request.json['latitude'],
        }
    lst.append(item)
    return jsonify({'item': item}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
