from flask import Flask, request, jsonify, render_template
import hashlib
import hmac
import time
import os

app = Flask(__name__)

# 🔐 SECRET KEY (NEVER EXPOSED TO FRONTEND)
SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_THIS_TO_REAL_SECRET")

# ⏰ 30-second time window
def time_block():
    return int(time.time() // 30)

# 🔐 CORE BANK-LEVEL GENERATOR
def generate_token(number: int):
    tb = time_block()

    message = f"{number}|{tb}".encode()

    # HMAC = bank-grade authentication primitive
    digest = hmac.new(
        SECRET_KEY.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    # Extra obfuscation layer (bank-style masking)
    final = hashlib.sha512(digest.encode()).hexdigest()

    return {
        "token": final,
        "time_block": tb
    }

# 🌐 FRONT PAGE
@app.route("/")
def home():
    return render_template("index.html")

# 🔐 SECURE API (NO LOGIC EXPOSED)
@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json
    number = int(data["number"])

    return jsonify(generate_token(number))

# ------------------------------------------------------------
if __name__ == "__main__":
    app.run()
