import datetime
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

project_model = api.model(
    "Project",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "desc": fields.String(),
        "budget": fields.Integer(),
    },
)

expense_model = api.model(
    "Expense",
    {
        "eid": fields.Integer(description="Expense ID"),
        "pid": fields.Integer(description="Project ID"),
        "cid": fields.Integer(required=True, description="Category ID"),
        "name": fields.String(required=True, description="Expense name"),
        "desc": fields.String(required=True, description="Expense description"),
        "amt": fields.Integer(required=True, description="Expense amount"),
        "created_at": fields.String(description="Date when expense was created"),
        "created_by": fields.String(description="User that created expense"),
        "updated_at": fields.String(description="Date when expense was last updated"),
        "updated_by": fields.String(description="User that last updated expense"),
    },
)

expense_input_model = api.model(
    "New Expense",
    {
        "cid": fields.Integer(required=True, description="Category ID"),
        "name": fields.String(required=True, description="Expense name"),
        "desc": fields.String(required=True, description="Expense description"),
        "amt": fields.Integer(required=True, description="Expense amount"),
        "user_id": fields.Integer(
            required=True, description="User ID of user that created the expense"
        ),
    },
)

expense_update_model = api.model(
    "Update Expense",
    {
        "id": fields.Integer(required=True, description="ID of expense"),
        "pid": fields.Integer(required=True, description="Project ID"),
        "cid": fields.Integer(required=True, description="Category ID"),
        "name": fields.String(required=True, description="Expense name"),
        "desc": fields.String(required=True, description="Expense description"),
        "amt": fields.Integer(required=True, description="Expense amount"),
        "updated_at": fields.String(description="Date when expense was last updated"),
        "updated_by": fields.String(description="User that last updated expense"),
        "user_id": fields.Integer(
            required=True, description="User ID of user that created the expense"
        ),
    },
)
expense_delete_model = api.model(
    "Delete Expense",
    {
        "id": fields.Integer(required=True, description="ID of expense")
    }
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
        expenses = []
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
                expenses.append(expense)
        return expenses

    @ns.doc("create_expense")
    @ns.expect(expense_input_model)
    @ns.marshal_with(expense_model, code=201)
    def post(self, project_id):
        """Create new project expense"""
        with connection.cursor() as cursor:
            # get user name
            user_name_query = (
                f"select name from user where id = {api.payload['user_id']};"
            )
            cursor.execute(user_name_query)
            row = cursor.fetchone()
            if row is None:
                return {}, 400
            name = row[0]
            # insert new expense object
            insert_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # insert_query = f"insert into expense (project_id, category_id, name, description, amount, created_at, created_by, updated_at, updated_by) select '{project_id}', '{api.payload['cid']}', '{api.payload['name']}', '{api.payload['desc']}', '{api.payload['amt']}', '{insert_datetime}', name, '{insert_datetime}', name from user where id = {api.payload['user_id']};"
            insert_query = f"insert into expense (project_id, category_id, name, description, amount, created_at, created_by, updated_at, updated_by) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            insert_data = (
                project_id,
                api.payload["cid"],
                api.payload["name"],
                api.payload["desc"],
                api.payload["amt"],
                insert_datetime,
                name,
                insert_datetime,
                name,
            )
            cursor.execute(insert_query, insert_data)
            # cursor.execute(insert_query)
            eid = cursor.lastrowid
            connection.commit()

            expense = {
                "eid": eid,
                "pid": project_id,
                "cid": api.payload["cid"],
                "name": api.payload["name"],
                "desc": api.payload["desc"],
                "amt": api.payload["amt"],
                "created_at": insert_datetime,
                "created_by": name,
                "updated_at": insert_datetime,
                "updated_by": name,
            }
        return expense, 201

    @ns.doc("update_expenses")
    @ns.expect(expense_update_model)
    @ns.marshal_with(expense_model, code=201)
    def put(self, project_id):
        """Edit current project expense"""
        with connection.cursor() as cursor:
            # get user name
            user_name_query = (
                f"select name from user where id = {api.payload['user_id']};"
            )
            cursor.execute(user_name_query)
            row = cursor.fetchone()
            if row is None:
                return {}, 400
            else: 
                name = row[0]
            # updating new expense object
            update_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_query = f"update expense set name = %s, description = %s, amount = %s, updated_at = %s where id = %s and project_id = %s;"
            update_data = (
                api.payload["name"],
                api.payload["desc"],
                api.payload["amt"],
                update_datetime,
                api.payload["id"],
                project_id
            )
            cursor.execute(update_query, update_data)
            connection.commit()

            expense = {
                "id": api.payload['id'],
                "pid": api.payload['pid'],
                "cid": api.payload["cid"],
                "name": api.payload["name"],
                "desc": api.payload["desc"],
                "amt": api.payload["amt"],
                "created_at": api.payload["created_at"],
                "created_by": name,
                "updated_at": update_datetime,
                "updated_by": name,
            }
        return expense, 201
    
    @ns.doc("delete_expenses")
    @ns.expect(expense_delete_model)
    @ns.marshal_with(expense_model, code=201)
    def put(self, project_id):
        """Delete current project expense"""
        with connection.cursor() as cursor:
            delete_query = f"delete from expense where id = %s and project_id = %s;"
            delete_data = (
                api.payload["id"],
                project_id
            )
            cursor.execute(delete_query, delete_data)
            connection.commit()

            expense = "successfully deleted"
        return expense, 201


if __name__ == "__main__":
    flask_app.run()
