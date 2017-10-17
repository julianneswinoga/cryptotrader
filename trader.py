#!/usr/bin/python

import bittrex as b

class Wallet(object):
    def __init__(self, coin_ticker, initial_value):
        self.ticker = coin_ticker
        self.value = initial_value

if __name__ == '__main__':
    my_bittrex = b.Bittrex(None, None, api_version='v1.1')
    print my_bittrex.get_markets()

    eth_wallet = Wallet('ETH', 0.4)
    zec_wallet = Wallet('ZEC', 0.5)

    print 'Hello!'
