#!/usr/bin/python

from bittrex import Bittrex
import json, sqlite3

class Wallet(object):
    def __init__(self, coin_ticker, initial_value):
        self.ticker = coin_ticker
        self.value = initial_value


class Market(object):
    def __init__(self, db_cursor, bittrex_connection, market_string):
        self.market_string = market_string
        self.table_name = market_string.replace('-', '_')
        self.db = db_cursor
        self.bit = bittrex_connection

        self.db.execute("CREATE TABLE IF NOT EXISTS %s (Id INT PRIMARY KEY, TimeStamp DATE, Total FLOAT, Price FLOAT, Quantity FLOAT, OrderType TEXT, FillType TEXT)" % self.table_name)

    def update(self):
        market_result = self.bit.get_market_history(self.market_string)['result']
        if len(market_result) > 0:
            keys = market_result[0].keys()
            db_statement = "INSERT INTO %s (%s) VALUES(%s)" % (self.table_name, ','.join(keys), ','.join([':%s' % s for s in keys]))
            self.db.executemany(db_statement, market_result)

    def get_data(self):
        self.db.execute("SELECT * FROM %s" % self.table_name)
        rows = self.db.fetchall()
        for row in rows:
            print row


if __name__ == '__main__':
    my_bittrex = Bittrex(api_key=None, api_secret=None)
    dbconn = sqlite3.connect('market.db')
    db = dbconn.cursor()

    eth_usd_market = Market(db, my_bittrex, 'USDT-ETH')
    eth_usd_market.update()

    eth_usd_market.get_data()

    # market_result = my_bittrex.get_market_history('USDT-ETH')['result']
    # print len(market_result)
    # print market_result[0]['TimeStamp']
    # print market_result[-1]['TimeStamp']
    # print market_result[0]

    # eth_wallet = Wallet('ETH', 0.4)
    # zec_wallet = Wallet('ZEC', 0.5)
