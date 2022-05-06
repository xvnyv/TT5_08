from flask import Flask, render_template, request,jsonify,session,url_for,redirect
from flask_restx import Api, Resource, fields
import mysql.connector
from functools import wraps
import jwt
from datetime import datetime, timedelta


flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'secretkey'
api = Api(
    app=flask_app,
    title="DBS Seed API",
    description="API for DBS Seed TechTrek Hackathon",
)

ns = api.namespace("ns1", description="NS1 description")



test_model = api.model(
    "Model",
    {
        "int_field": fields.Integer(readonly=True, description="Integer Field 1"),
        "str_field": fields.String(required=True, description="String Field 1"),
    },
)

connection = mysql.connector.connect(host='13.58.31.172',database='project_expenses',user='root',password='')

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "missing token"}), 403
        try:
            data = jwt.decode(token,flask_app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped


@flask_app.route('/login',methods =['GET','POST'])
def login():
    
    if request.method == 'POST':
        content = request.json
        username = content['username']
        password = content['password']
        
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s',(username))
        account = cursor.fetchone()
        
        if account and password == account['password']:
            session['loggedin'] = True
            token =jwt.encode({
                'user': username,
                'exp': datetime.utcnow() + timedelta(seconds=600)
            })
            
        else:
            return "wrong password or username"
            
                
    return render_template('login.html')######  

@flask_app.route('/logout')
def logout():
    
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    
    return redirect(url_for('login'))

## some home route that requires login?

          




items = [
    {"int_field": 1, "str_field": "str1"},
    {"int_field": 2, "str_field": "str2"},
]


@ns.route("/")
class ItemList(Resource):
    """Show list of items and allow creation of item"""

    @ns.doc("list_items")
    @ns.marshal_list_with(test_model)
    def get(self):
        """List all items"""
        return items

    @ns.doc("create_item")
    @ns.expect(test_model)
    @ns.marshal_with(test_model, code=201)
    def post(self):
        """Create new item"""
        items.append(api.payload)
        return items, 201


@ns.route("/<int:int_field>")
@ns.response(404, "Item not found")
@ns.param("int_field", "Int Field 1")
class Item(Resource):
    """Show a single item and allow deletion and update of item"""

    @ns.doc("get_item")
    @ns.marshal_with(test_model)
    def get(self, int_field):
        """Fetch a given item"""
        for item in items:
            if item["int_field"] == int_field:
                return item
        return "", 404

    @ns.doc("delete_item")
    @ns.response(204, "Item deleted")
    def delete(self, int_field):
        """Delete a given item"""
        delete_item = None
        for item in items:
            if item["int_field"] == int_field:
                delete_item = item
        if delete_item is not None:
            items.remove(delete_item)
            return "", 204
        return "", 404

    @ns.expect(test_model)
    @ns.marshal_with(test_model)
    def put(self, int_field):
        """Update a given item"""
        for item in items:
            if item["int_field"] == int_field:
                item.update(api.payload)
                return item
        return "", 404


if __name__ == "__main__":
    flask_app.run()
