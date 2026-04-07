from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database
users = {"admin": "password123"}

@app.route("/")
def home():
    return "Welcome to Sample App"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/search")
def search():
    query = request.args.get("q")
    return jsonify({"results": f"Results for {query}"}), 200

@app.route("/payment", methods=["POST"])
def payment():
    amount = request.json.get("amount")
    if amount and amount > 0:
        return jsonify({"status": "Payment successful"}), 200
    return jsonify({"status": "Payment failed"}), 400

if __name__ == "__main__":
    app.run(debug=True)
