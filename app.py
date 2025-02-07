from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# Habilita o CORS para todas as rotas
CORS(app)

# Sua chave da API do CoinMarketCap
API_KEY = '1180bf54-7bb8-45b9-8d22-bf6213ae4358'
COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

@app.route("/get_price", methods=["GET"])
def get_price():
    try:
        # Solicitação para obter os preços das criptomoedas
        response = requests.get(COINMARKETCAP_API_URL, headers={
            'X-CMC_PRO_API_KEY': API_KEY,
            'Accept': 'application/json',
        }, params={
            'symbol': 'BTC,ETH,SOL',  # Coloque os símbolos das criptos que você deseja (Bitcoin, Ethereum, Solana)
            'convert': 'USD'
        })

        # Verifica se a requisição foi bem sucedida
        print("Status Code:", response.status_code)  # Imprime o código de status da resposta
        
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch data from CoinMarketCap. Status Code: {response.status_code}"}), 500
        
        data = response.json()

        # Monta o dicionário de resposta com os preços de cada criptomoeda
        prices = {}
        for coin in data['data']:
            symbol = coin['symbol']
            prices[symbol] = coin['quote']['USD']['price']

        return jsonify(prices)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
