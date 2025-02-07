from flask import Flask, jsonify
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Add CORS to your Flask app
CORS(app)  # Now all routes accept requests from different origins

# Your API key
API_KEY = '1180bf54-7bb8-45b9-8d22-bf6213ae4358'

# CoinMarketCap API endpoint
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Authentication headers
headers = {
    'X-CMC_PRO_API_KEY': API_KEY,
    'Accept': 'application/json',
}

# Function to get cryptocurrency prices
def get_crypto_prices():
    # Symbols of the cryptocurrencies you want to query
    parameters = {
        'symbol': 'BTC,ETH,SOL',  # Querying multiple cryptocurrencies
        'convert': 'USD'
    }

    # GET request to the API
    response = requests.get(API_URL, headers=headers, params=parameters)

    # Log status code and response body for debugging
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code == 200:
        data = response.json()['data']
        # Format prices and include market changes
        prices = {
            'bitcoin': round(data['BTC']['quote']['USD']['price']),  # Round to integer
            'ethereum': round(data['ETH']['quote']['USD']['price'], 2),  # 2 decimal places
            'solana': round(data['SOL']['quote']['USD']['price'], 2),  # 2 decimal places
            'bitcoin_change_24h': round(data['BTC']['quote']['USD']['percent_change_24h'], 2),  # 24h change
            'ethereum_change_24h': round(data['ETH']['quote']['USD']['percent_change_24h'], 2),  # 24h change
            'solana_change_24h': round(data['SOL']['quote']['USD']['percent_change_24h'], 2),  # 24h change
            'bitcoin_change_7d': round(data['BTC']['quote']['USD']['percent_change_7d'], 2),  # 7d change
            'ethereum_change_7d': round(data['ETH']['quote']['USD']['percent_change_7d'], 2),  # 7d change
            'solana_change_7d': round(data['SOL']['quote']['USD']['percent_change_7d'], 2),  # 7d change
            'bitcoin_change_1h': round(data['BTC']['quote']['USD']['percent_change_1h'], 2),  # 1h change
            'ethereum_change_1h': round(data['ETH']['quote']['USD']['percent_change_1h'], 2),  # 1h change
            'solana_change_1h': round(data['SOL']['quote']['USD']['percent_change_1h'], 2)  # 1h change
        }
        return prices
    else:
        return {'error': 'Unable to fetch data'}

@app.route('/get_price', methods=['GET'])
def get_price():
    prices = get_crypto_prices()
    return jsonify(prices)

if __name__ == '__main__':
    app.run(debug=True)
