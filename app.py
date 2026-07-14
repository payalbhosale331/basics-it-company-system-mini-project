from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)


# Database Creation

def create_database():

    con = sqlite3.connect("company.db")
    cur = con.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        department TEXT
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        company TEXT,
        phone TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        technology TEXT,
        status TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        employee TEXT,
        status TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee TEXT,
        date TEXT,
        status TEXT
    )
    """)



    con.commit()
    con.close()



create_database()



@app.route("/")
def home():

    return render_template("index.html")



# EMPLOYEE MODULE

@app.route("/add_employee",methods=["POST"])
def add_employee():

    data=request.json


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    """
    INSERT INTO employees
    (name,email,department)
    VALUES(?,?,?)
    """,
    (
    data["name"],
    data["email"],
    data["department"]
    )
    )


    con.commit()
    con.close()


    return jsonify(
    {"message":"Employee Added Successfully"}
    )





@app.route("/employees")
def get_employee():


    con=sqlite3.connect("company.db")

    cur=con.cursor()

    cur.execute("SELECT * FROM employees")


    data=cur.fetchall()


    con.close()


    return jsonify(data)






# CLIENT MODULE


@app.route("/add_client",methods=["POST"])
def add_client():


    data=request.json


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    """
    INSERT INTO clients
    (name,company,phone)
    VALUES(?,?,?)
    """,
    (
    data["name"],
    data["company"],
    data["phone"]
    )
    )


    con.commit()

    con.close()


    return jsonify(
    {"message":"Client Added"}
    )




@app.route("/clients")
def clients():


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    "SELECT * FROM clients"
    )


    data=cur.fetchall()

    con.close()


    return jsonify(data)






# PROJECT MODULE


@app.route("/add_project",methods=["POST"])
def add_project():


    data=request.json


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    """
    INSERT INTO projects
    (name,technology,status)
    VALUES(?,?,?)
    """,
    (
    data["name"],
    data["technology"],
    data["status"]
    )
    )


    con.commit()

    con.close()


    return jsonify(
    {"message":"Project Created"}
    )






@app.route("/projects")
def projects():


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    "SELECT * FROM projects"
    )


    data=cur.fetchall()

    con.close()


    return jsonify(data)







# TASK MODULE


@app.route("/add_task",methods=["POST"])
def add_task():


    data=request.json


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    """
    INSERT INTO tasks
    (title,employee,status)
    VALUES(?,?,?)
    """,
    (
    data["title"],
    data["employee"],
    data["status"]
    )
    )


    con.commit()

    con.close()


    return jsonify(
    {"message":"Task Added"}
    )




@app.route("/tasks")
def tasks():


    con=sqlite3.connect("company.db")

    cur=con.cursor()


    cur.execute(
    "SELECT * FROM tasks"
    )


    data=cur.fetchall()


    con.close()


    return jsonify(data)





if __name__=="__main__":

    app.run(debug=True)