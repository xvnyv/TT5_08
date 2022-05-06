from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_restx import Api, Resource, fields
import mysql.connector
from functools import wraps
import jwt
from datetime import datetime, timedelta


flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = "secretkey"
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
        "user_id": fields.Integer(
            required=True, description="User ID of user that created the expense"
        ),
    },
)

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return jsonify({"message": "missing token"}), 403
        try:
            data = jwt.decode(token, flask_app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Invalid token"}), 403
        return func(*args, **kwargs)

    return wrapped


@flask_app.route("/login", methods=["POST"])
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
                "user": user["username"],
                "exp": datetime.utcnow() + timedelta(seconds=600),
            },
            flask_app.config["SECRET_KEY"],
        )
        user["token"] = token
        return user

      
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


if __name__ == "__main__":
    flask_app.run(debug=True)
