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
    },
)

# eid, pid, cid, name, desc, amt, created_date, created_user, updated_date, updated_user

expense_model = api.model(
    "Expense",
    {
        "eid": fields.Integer(),
        "pid": fields.Integer(),
        "cid": fields.Integer(),
        "name": fields.String(),
        "desc": fields.String(),
        "amt": fields.Integer(),
        "created_at": fields.String(),
        "created_by": fields.String(),
        "updated_at": fields.String(),
        "updated_by": fields.String(),
    },
)


@ns.route("/projects/<int:user_id>")
class ProjectList(Resource):
    """Show list of projects under a user"""

    @ns.doc("list_projects")
    @ns.marshal_list_with(project_model)
    def get(self, user_id):
        """List all items"""
        proj_list = []
        get_project_list_query = f"select * from project where user_id = {user_id};"
        with connection.cursor() as cursor:
            cursor.execute(get_project_list_query)
            for (pid, _, pname, pdesc, pbudget) in cursor:
                proj = {
                    "id": int(pid),
                    "name": pname,
                    "desc": pdesc,
                    "budget": int(pbudget),
                }
                proj_list.append(proj)

        return proj_list


@ns.route("/expense/<int:project_id>")
@ns.response(404, "Item not found")
@ns.param("project_id", "Project ID")
class ProjectExpense(Resource):
    """Show a single project expense and allow addition, deletion and update of project expense"""

    @ns.doc("get_expense")
    @ns.marshal_with(expense_model)
    def get(self, project_id):
        """Fetch a given project expense"""
        get_expense_query = f"select * from expense where project_id = {project_id};"
        with connection.cursor() as cursor:
            cursor.execute(get_expense_query)
            for (
                eid,
                pid,
                cid,
                name,
                desc,
                amt,
                created_date,
                created_user,
                updated_date,
                updated_user,
            ) in cursor:
                expense = {
                    "eid": eid,
                    "pid": pid,
                    "cid": cid,
                    "name": name,
                    "desc": desc,
                    "amt": amt,
                    "created_at": created_date,
                    "created_by": created_user,
                    "updated_at": updated_date,
                    "updated_by": updated_user,
                }
                return expense
        return {}, 404


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
