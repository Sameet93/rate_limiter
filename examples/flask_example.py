# File: examples/flask_example.py
from flask import Flask, request, jsonify
from rate_limiter import rate_limit, MemoryCache

app = Flask(__name__)
cache = MemoryCache()

def get_remote_addr():
    return "ip:" + request.remote_addr

@app.route("/flask-endpoint")
@rate_limit(
    limit=10,
    period=60,
    identifier=get_remote_addr,
    cache=cache,
    auto_ban=True,
    ban_threshold=20,
    ban_duration=120
)
def my_flask_endpoint():
    return jsonify(message="Hello from Flask!")

if __name__ == "__main__":
    app.run(debug=True)

