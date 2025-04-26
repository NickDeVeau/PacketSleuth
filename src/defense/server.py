# src/defense/server.py
"""
Tiny Flask HTTPS server with HSTS header.
"""

from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def home() -> Response:
    resp = Response("<h1>Hello from secure server</h1>")
    resp.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    return resp

if __name__ == "__main__":
    context = ("certs/server.crt", "certs/server.key")
    app.run(host="0.0.0.0", port=4443, ssl_context=context)
