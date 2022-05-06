from flask import Flask
from flask_restx import Api, Resource, fields
import mysql.connector

flask_app = Flask(__name__)
api = Api(
    app=flask_app,
    title="DBS Seed API",
    description="API for DBS Seed TechTrek Hackathon",
)

ns = api.namespace("", description="Projects endpoints")

connection = mysql.connector.connect(
    host="13.58.31.172", database="project_expenses", user="root", password=""
)

# test_model = api.model(
#     "Model",
#     {
#         "int_field": fields.Integer(readonly=True, description="Integer Field 1"),
#         "str_field": fields.String(required=True, description="String Field 1"),
#     },
# )

project_model = api.model(
    "Project",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "desc": fields.String(),
        "budget": fields.Integer(),
        "user": fields.String(),
    },
)


@ns.route("/projects")
class ProjectList(Resource):
    """Show list of projects and allow creation of project"""

    @ns.doc("list_projects")
    @ns.marshal_list_with(project_model)
    def get(self):
        """List all items"""
        proj_list = []
        get_project_list_query = "select * from (project p inner join (select id, name as user from user) u on p.user_id = u.id);"
        with connection.cursor() as cursor:
            cursor.execute(get_project_list_query)
            for (pid, _, pname, pdesc, pbudget, _, uname) in cursor:
                proj = {
                    "id": int(pid),
                    "name": pname,
                    "desc": pdesc,
                    "budget": pbudget,
                    "user": uname,
                }
                proj_list.append(proj)

        return proj_list


#     @ns.doc("create_item")
#     @ns.expect(test_model)
#     @ns.marshal_with(test_model, code=201)
#     def post(self):
#         """Create new item"""
#         items.append(api.payload)
#         return items, 201


# @ns.route("/expense/<int:project_id>")
# @ns.response(404, "Item not found")
# @ns.param("project_id", "Project ID")
# class ProjectExpense(Resource):
#     """Show a single project expense and allow addition, deletion and update of project expense"""

#     @ns.doc("get_item")
#     @ns.marshal_with(test_model)
#     def get(self, int_field):
#         """Fetch a given item"""
#         for item in items:
#             if item["int_field"] == int_field:
#                 return item
#         return "", 404

# @ns.doc("create_expense")
# @ns.expect(test_model)
# @ns.marshal_with(test_model, code=201)
# def post(self):
#     """Create new item"""
#     items.append(api.payload)
#     return items, 201

# @ns.doc("delete_item")
# @ns.response(204, "Item deleted")
# def delete(self, int_field):
#     """Delete a given item"""
#     delete_item = None
#     for item in items:
#         if item["int_field"] == int_field:
#             delete_item = item
#     if delete_item is not None:
#         items.remove(delete_item)
#         return "", 204
#     return "", 404

# @ns.expect(test_model)
# @ns.marshal_with(test_model)
# def put(self, int_field):
#     """Update a given item"""
#     for item in items:
#         if item["int_field"] == int_field:
#             item.update(api.payload)
#             return item
#     return "", 404


if __name__ == "__main__":
    flask_app.run()
