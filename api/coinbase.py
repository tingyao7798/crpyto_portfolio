""" wrapper module that calls coinbase api"""
# core modules
import logging

# third party modules
from coinbase.wallet.client import Client

# self modules
from api.coinmarketcap import Coinmarketcap

class Coinbase:
    """ wrapper class on top of Bittrex
    Init:
        api_key: string
        api_secret: string
    """
    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret

    def _get_balance(self):
        """ method to get coinbase balances
        Returns:
            wallet: list of dict e.g.
                  [{"balance": {
                    "amount": "0.00058000",
                    "currency": "BTC"
                    },
                    "created_at": "2017-07-11T13:27:36Z",
                    "currency": "BTC",
                    "id": "3abaaa8a-d9e4-58d5-9143-df3ca8a3b67f",
                    "name": "BTC Wallet",
                    "native_balance": {
                        "amount": "12.81",
                        "currency": "SGD"
                    },
                    "primary": true,
                    "resource": "account",
                    "resource_path": "/v2/accounts/3abaaa8a-d9e4-58d5-9143-df3ca8a3b67f",
                    "type": "wallet",
                    "updated_at": "2017-12-13T09:31:31Z"}]
        """

        logger = logging.getLogger(__name__)
        logger.debug("Retrieving Coinbase account balances...")
        client = Client(self.__api_key, self.__api_secret)
        resp = client.get_accounts().data

        return resp

    def _format_wallet(self):
        """ method to format wallet
        Args:
            wallet: list of dict
        Returns:
            wallet_dict: dict: float e.g.{'iot':222}
        """
        wallet = self._get_balance()

        # init wallet dict
        wallet_dict = {}
        for coin in wallet:
            amount = float(coin['balance']['amount'])
            if amount > 0.:
                wallet_dict.update({coin['balance']['currency'].upper(): amount})

        return wallet_dict

    def get_wallet_value(self):
        """ method to get wallet value
        Args:
            wallet: list of dict
        Returns:
            wallet_value: float
        """
        # get wallet balance
        wallet = self. _format_wallet()

        # get latest prices from coinmarketcap
        cmc_client = Coinmarketcap()
        ticker_prices = cmc_client.get_ticker_prices()

        wallet_value = 0.

        for coin, amt in wallet.items():
            price_usd = float(ticker_prices[coin])
            wallet_value = wallet_value + (amt * price_usd)

        return wallet_value


    