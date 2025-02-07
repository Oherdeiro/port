from flask import Flask, jsonify
import requests
from flask_cors import CORS  # Importe o CORS

app = Flask(__name__)

# Adiciona o CORS ao seu app Flask
CORS(app)  # Agora todas as rotas aceitam requisições de origens diferentes

# Sua chave da API
API_KEY = '1180bf54-7bb8-45b9-8d22-bf6213ae4358'

# Endpoint da API da CoinMarketCap
API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Cabeçalhos para autenticação
headers = {
    'X-CMC_PRO_API_KEY': API_KEY,
    'Accept': 'application/json',
}

# Função para obter o preço das criptomoedas
def get_crypto_prices():
    # Símbolos das criptomoedas que você deseja consultar
    parameters = {
        'symbol': 'BTC,ETH,SOL',  # Usando 'symbol' para consultar múltiplas criptomoedas
        'convert': 'USD'
    }

    # Requisição GET para a API
    response = requests.get(API_URL, headers=headers, params=parameters)

    # Logando o código de status e o conteúdo da resposta para depuração
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code == 200:
        data = response.json()['data']
        # Formatar os preços conforme necessário
        prices = {
            'bitcoin': round(data['BTC']['quote']['USD']['price']),  # Arredondar para inteiro
            'ethereum': round(data['ETH']['quote']['USD']['price'], 2),  # 2 casas decimais
            'solana': round(data['SOL']['quote']['USD']['price'], 2)  # 2 casas decimais
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
