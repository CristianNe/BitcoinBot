import requests
import json

class HttpService:
    def __init__(self):
        self.__URL = "https://api.coingecko.com/api/v3/coins/bitcoin"

    def getMarketStats(self):
        request = requests.get(self.__URL)
        if request.status_code == 200:
          response = json.loads(request.text)
          price = response["market_data"]["current_price"]["usd"]
          ath = response["market_data"]["ath"]["usd"]
          print(f"checked price:\nprice: ${price}\nath: ${ath}")
          return price, ath

        elif request.status_code >= 400:
            with open('ressources/error.log', 'w') as f:
                f.write(request.text)
            return -1, -1





