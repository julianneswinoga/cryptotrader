#!/usr/bin/python

from bittrex import Bittrex
import matplotlib.pyplot as plt
import datetime as dt
import json, sqlite3, pprint

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
            for i, result in enumerate(market_result):  # Prep TimeStamp data to always have a microsecond
                if '.' not in result['TimeStamp']:
                    market_result[i]['TimeStamp'] += '.0'

            db_statement = "INSERT INTO %s (%s) VALUES(%s)" % (self.table_name, ','.join(keys), ','.join([':%s' % s for s in keys]))
            self.db.executemany(db_statement, market_result)

    def get_data(self):
        self.db.execute("SELECT * FROM %s" % self.table_name)
        rows = self.db.fetchall()
        return [(r['TimeStamp'], r['Price']) for r in rows]


if __name__ == '__main__':
    my_bittrex = Bittrex(api_key=None, api_secret=None)
    dbconn = sqlite3.connect('market.db')
    dbconn.row_factory = sqlite3.Row
    db = dbconn.cursor()

    eth_usd_market = Market(db, my_bittrex, 'USDT-ETH')
    eth_usd_market.update()

    data = eth_usd_market.get_data()
    pprint.pprint(data)
    print len(data)
    dates = [d[0] for d in data]
    x = [dt.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S.%f').date() for d in dates]
    y = [d[1] for d in data]

    plt.gcf().autofmt_xdate()
    plt.plot(x, y)
    plt.show()

    # market_result = my_bittrex.get_market_history('USDT-ETH')['result']
    # print len(market_result)
    # print market_result[0]['TimeStamp']
    # print market_result[-1]['TimeStamp']
    # print market_result[0]

    # eth_wallet = Wallet('ETH', 0.4)
    # zec_wallet = Wallet('ZEC', 0.5)
