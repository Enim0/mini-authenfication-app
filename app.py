from flask import Flask, request
import auth_system
    
app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login =  request.form["login"]
        password = request.form["passwords"]
        


if __name__ == "__main__":
    app.run(debug=True)