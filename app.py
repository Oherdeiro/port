import os
from flask import Flask, jsonify
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all domains (you can also specify specific domains)
CORS(app)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@app.route("/get_price", methods=["GET"])
def get_price():
    try:
        response = requests.get(COINGECKO_API_URL, params={
            'ids': 'bitcoin,ethereum,solana',
            'vs_currencies': 'usd'
        })
        data = response.json()

        return jsonify({
            "bitcoin": data['bitcoin']['usd'],
            "ethereum": data['ethereum']['usd'],
            "solana": data['solana']['usd']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
