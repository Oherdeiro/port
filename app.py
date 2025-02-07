from flask import Flask, jsonify
import requests

app = Flask(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@app.route("/get_price", methods=["GET"])
def get_price():
    try:
        # Consultando preços de Solana, Ethereum e Bitcoin
        response = requests.get(COINGECKO_API_URL, params={
            'ids': 'bitcoin,ethereum,solana',
            'vs_currencies': 'usd'
        })
        
        data = response.json()

        # Retorna os preços em formato JSON
        return jsonify({
            "bitcoin": data['bitcoin']['usd'],
            "ethereum": data['ethereum']['usd'],
            "solana": data['solana']['usd']
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
