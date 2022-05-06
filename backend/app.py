from flask import Flask, render_template, request
from flask_restx import Api, Resource, fields
import mysql.connector
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

flask_app = Flask(__name__)
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
            ## return JWT token
            access_token = create_access_token(identity = username)
            refresh_token = create_refresh_token(identity =username)
            
            return {
                'message' : f' Hello {username}!',
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }
        
        else:
            return{'message': "wrong credentials"}    
        
    return ('hello world')    
        
@flask_app.route('/logout',methods = ['GET','POST'])
def logout();




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
