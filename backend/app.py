from flask import Flask
from flask_restx import Api, Resource, fields
import mysql.connector

flask_app = Flask(__name__)
api = Api(
    app=flask_app,
    title="DBS Seed API",
    description="API for DBS Seed TechTrek Hackathon",
)

ns = api.namespace("ns1", description="NS1 description")

connection = mysql.connector.connect(host='13.58.31.172',database='project_expenses',user='root',password='')


test_model = api.model(
    "Model",
    {
        "int_field": fields.Integer(readonly=True, description="Integer Field 1"),
        "str_field": fields.String(required=True, description="String Field 1"),
    },
)

cnx = mysql.connector.connect(user="root")

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


#update database record
# @flask_app.route('/update',['PUT'])
def update(self, params):
    try:
        mycursor = connection.cursor()
        id = params.id
        pid = params.project_id
        cid = params.category_id
        name = params.name
        description = params.name
        amount = params.amount
        uexpense = "update expense set name = %s, description = %s, amount = %s, updated_at = now() where project_id = %s and category_id = %s;"
        val = (name, description, amount, pid, cid)
        mycursor.execute(uexpense, val)
        connection.commit()
        print("Update successful")
    except:
        print("failed to update")

#delete database record
# @flask_app.route('/update',['POST'])
def update(self, params):
    try:
        mycursor = connection.cursor()
        id = params.id
        dexpense = "delete from expense where id = %s;"
        val = (id)
        mycursor.execute(dexpense, val)
        connection.commit()
        print("Update successful")
    except:
        print("failed to update")

if __name__ == "__main__":
    flask_app.run()
