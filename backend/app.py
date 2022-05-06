from flask import Flask, request, session
from flask_restx import Api, Resource, fields, cors
from flask_cors import CORS, cross_origin
import mysql.connector
from functools import wraps
import jwt
from datetime import datetime, timedelta


flask_app = Flask(__name__)
cors = CORS(flask_app)
flask_app.config["SECRET_KEY"] = "secretkey"
api = Api(
    app=flask_app,
    title="DBS Seed API",
    description="API for DBS Seed TechTrek Hackathon",
)

ns = api.namespace("", description="Projects endpoints", decorators=[cross_origin()])
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

user_model = api.model(
    "User",
    {
        "id": fields.Integer(description="User ID"),
        "username": fields.String(description="Username for login"),
        "name": fields.String(description="Name of user"),
        "appointment": fields.String(description="Appointment of user"),
        "token": fields.String(description="JWT authentication token"),
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
    "Delete Expense", {"id": fields.Integer(required=True, description="ID of expense")}
)


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        auth = request.headers.get("Authorization", None)
        if auth is None:
            return {}, 401

        token = auth.split(" ")[1]
        try:
            data = jwt.decode(
                token, flask_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            kwargs["user_id"] = data.get("user", None)
        except Exception as err:
            print(err)
            return {}, 401
        return func(*args, **kwargs)

    return wrapped


@flask_app.route("/login", methods=["POST"])
@cross_origin()
def login():
    if request.method == "POST":
        content = request.json
        input_username = content["username"]
        input_password = content["password"]

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user WHERE username='{input_username}';")
        account = cursor.fetchone()

        if account is None:
            return {}, 401

        user = {
            "id": account[0],
            "username": account[1],
            "name": account[3],
            "appointment": account[4],
        }

        password = account[2]

        if input_password != password:
            return {}, 401

        session["loggedin"] = True
        token = jwt.encode(
            {
                "user": user["id"],
                "exp": datetime.utcnow() + timedelta(seconds=3600),
            },
            flask_app.config["SECRET_KEY"],
        )
        user["token"] = token
        return user


@ns.route("/projects")
class ProjectList(Resource):
    """Show list of projects under a user"""

    # @ns.marshal_list_with(project_model)
    @ns.doc("list_projects")
    @check_for_token
    def get(self, **kwargs):
        """List all items"""
        if kwargs["user_id"] is None:
            return "Invalid token", 401

        proj_list = []
        get_project_list_query = (
            f"select * from project where user_id = '{kwargs['user_id']}';"
        )
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

    # @ns.marshal_with(expense_model)
    @ns.doc("get_expense")
    @check_for_token
    def get(self, project_id, **kwargs):
        """Fetch a given project expense"""
        if kwargs["user_id"] is None:
            return "Invalid token", 401

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
                    "created_at": created_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "created_by": created_user,
                    "updated_at": updated_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_by": updated_user,
                }
                expenses.append(expense)
        print(expenses)
        return expenses

    # @ns.marshal_with(expense_model, code=201)
    @ns.doc("create_expense")
    @ns.expect(expense_input_model)
    @check_for_token
    def post(self, project_id, **kwargs):
        """Create new project expense"""
        if kwargs["user_id"] is None:
            return "Invalid token", 401

        with connection.cursor() as cursor:
            # get user name
            user_name_query = f"select name from user where id = {kwargs['user_id']};"
            cursor.execute(user_name_query)
            row = cursor.fetchone()
            if row is None:
                return {}, 400
            name = row[0]
            # insert new expense object
            insert_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    # @ns.marshal_with(expense_model, code=201)
    @ns.doc("update_expenses")
    @ns.expect(expense_update_model)
    @check_for_token
    def put(self, project_id, **kwargs):
        """Edit current project expense"""
        if kwargs["user_id"] is None:
            return "Invalid token", 401

        with connection.cursor() as cursor:
            # get user name
            user_name_query = f"select name from user where id = {kwargs['user_id']};"
            cursor.execute(user_name_query)
            row = cursor.fetchone()
            if row is None:
                return {}, 400
            else:
                name = row[0]

            # updating new expense object
            update_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_query = f"update expense set name = %s, description = %s, amount = %s, updated_at = %s, updated_by = %s where id = %s and project_id = %s;"
            update_data = (
                api.payload["name"],
                api.payload["desc"],
                api.payload["amt"],
                update_datetime,
                name,
                api.payload["id"],
                project_id,
            )
            cursor.execute(update_query, update_data)
            connection.commit()

            expense = {
                "id": api.payload["id"],
                "pid": api.payload["pid"],
                "cid": api.payload["cid"],
                "name": api.payload["name"],
                "desc": api.payload["desc"],
                "amt": api.payload["amt"],
                "updated_at": update_datetime,
                "updated_by": name,
            }
        return expense, 201

    # @ns.marshal_with(expense_model, code=201)
    @ns.doc("delete_expenses")
    @ns.expect(expense_delete_model)
    @check_for_token
    def delete(self, project_id, **kwargs):
        """Delete current project expense"""
        if kwargs["user_id"] is None:
            return "Invalid token", 401

        with connection.cursor() as cursor:
            delete_query = f"delete from expense where id = %s and project_id = %s;"
            delete_data = (api.payload["id"], project_id)
            cursor.execute(delete_query, delete_data)
            connection.commit()

            expense = "successfully deleted"
        return expense


if __name__ == "__main__":
    flask_app.run(debug=True)
