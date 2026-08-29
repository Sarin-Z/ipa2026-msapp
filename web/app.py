from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
db = client["ipa2026_db"]
routers = db["routers"]

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
        routers.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_comment():
    try:
        doc_id = request.form.get("id")
        routers.delete_one({"_id": ObjectId(doc_id)})
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)