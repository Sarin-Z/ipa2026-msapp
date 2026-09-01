import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]
routers = db["routers"]
interface_status = db["interface_status"]


@app.route("/")
def main():
    data = list(routers.find({}, {"password": 0}))
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if (ip and username) and password:
        routers.insert_one(
            {"ip": ip, "username": username, "password": password}
        )
    return redirect(url_for("main"))


@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        doc_id = request.form.get("id")
        routers.delete_one({"_id": ObjectId(doc_id)})
    except Exception:
        pass
    return redirect(url_for("main"))


@app.route("/router/<router_ip>")
def router_detail(router_ip):

    records = list(
        interface_status.find({"router_ip": router_ip})
        .sort("timestamp", -1)
        .limit(3)
    )
    return render_template(
        "router_detail.html", router_ip=router_ip, records=records
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
