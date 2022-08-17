# -*- coding: utf-8 -*-
import matplotlib
from time import sleep
from datetime import datetime, time, timedelta
from dateutil import parser
import numpy as np
import pandas as pd
from pandas import *
from numpy import *
import os
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import talib as ta
matplotlib.use('TkAgg')
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

# ----------------------------------------------------------------------------
# backtrade system
class backtrade(object):
    def __init__(self):
        self._Open = []
        self._High = []
        self._Low = []
        self._Close = []
        self._Volume = []
        self._Dt = []
        self._ema12_list = [0]
        self._ema26_list = [0]
        self._fast_dif_list = [0]
        self._slow_dea_list = [0]
        self._macd_column_list = [0]
        self._order_number = 0
        self._Money = 10000
        self._current_orders = {}
        self._history_orders = {}
        self.key = ''
        self._pnl = []


    def getbar(self, bar_path):
        data = pd.read_csv(
                bar_path,
                parse_dates=['datetime'],
                index_col='datetime'
            )
        for index, row in data.iterrows():
            self._Open.insert(0, row['open'])
            self._High.insert(0, row['high'])
            self._Low.insert(0, row['low'])
            self._Close.insert(0, row['close'])
            self._Volume.insert(0, row['volume'])
            self._Dt.insert(0, index)
        # plt.rcParams['font.sans-serif'] = [u'SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # plt.figure(figsize=(9, 6))
        # plt.plot(self._Dt, self._Close, 'b-', label='5分钟价格曲线', lw=2.0)
        # plt.axis('tight')
        # plt.xticks(fontsize=14)
        # plt.yticks(fontsize=14)
        # plt.xlabel(u'时间轴', fontsize=14)
        # plt.ylabel(u'价格/元', fontsize=14)
        # plt.title(u'恒生互联网etf价格走势')
        # plt.legend(loc=0, fontsize=14)
        # plt.grid()
        # plt.show()

    def strategy(self):
        # Macd definition
        # can't fix the problem of big bump of macd curse
        for i in range(len(self._Close)-1, 0, -1):
            ema12 = self._ema12_list[-1]*11/13+self._Close[i]*2/13
            ema26 = self._ema26_list[-1]*25/27+self._Close[i]*2/27
            fast_dif = ema12 - ema26
            slow_dea = self._slow_dea_list[-1]*8/10+fast_dif*2/10
            macd_column = (fast_dif - slow_dea) * 2
            self._ema12_list.append(ema12)
            self._ema26_list.append(ema26)
            self._fast_dif_list.append(fast_dif)
            self._slow_dea_list.append(slow_dea)
            self._macd_column_list.append(macd_column)
        self._ema12_list.reverse()
        self._ema26_list.reverse()
        self._fast_dif_list.reverse()
        self._slow_dea_list.reverse()
        self._macd_column_list.reverse()
        self._ema12_list = self._ema12_list[:218]
        self._ema26_list = self._ema26_list[:218]
        self._fast_dif_list = self._fast_dif_list[:218]
        self._slow_dea_list = self._slow_dea_list[:218]
        self._macd_column_list = self._macd_column_list[:218]
        self._Dt = self._Dt[:218]
        self._Open = self._Open[:218]
        self._High = self._High[:218]
        self._Low = self._Low[:218]
        self._Close = self._Close[:218]
        self._Volume = self._Volume[:218]



    def buy(self, buy_time, price, volume):
        # total money
        # maximum number of buying
        self._order_number += 1
        self.key = "order" + str(self._order_number)
        self._current_orders[self.key] = {
            "buy_datetime": buy_time,
            "buy_price": price,
            "volume": volume
        }


    def sell(self, sell_time, price):
        self._current_orders[self.key]['sell_price'] = price
        self._current_orders[self.key]['sell_datetime'] = sell_time
        self._current_orders[self.key]['pnl'] = \
            (price - self._current_orders[self.key]['buy_price']) \
            * self._current_orders[self.key]['volume'] \
            - (price + self._current_orders[self.key]['buy_price']) \
            * self._current_orders[self.key]['volume'] * 3 / 10000
        # move order from current orders to history orders
        self._pnl.append(self._current_orders[self.key]['pnl'])
        self._history_orders[self.key] = self._current_orders.pop(self.key)


    def run_backtrade(self):
        # if self._fast_dif_list[i] > self._slow_dea_list[i] and self._macd_column_list[i] > 0:
        for i in range(len(self._Dt)-1, -1, -1):
            if self._macd_column_list[i] > 0:
                if self._current_orders:
                    pass
                else:
                    self.buy(self._Dt[i], self._Close[i], self._Money / self._Close[i])
            else:
                if self._current_orders:
                    self.sell(self._Dt[i], self._Close[i])
                else:
                    pass
        pnl_sum = []
        for j in range(len(self._pnl)):
            pnl_sum.append(sum(self._pnl[:j]))
        plt.rcParams['font.sans-serif'] = [u'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(18, 12))
        plt.grid()
        ax1 = plt.subplot(5, 1, 1)
        ax1.plot(self._Dt, self._Close, 'b-', label='close price', lw=2.0)
        ax1.legend(loc=0, fontsize=14)
        ax2 = plt.subplot(5, 1, 2)
        ax2.bar(x=self._Dt, height=self._Volume)
        ax2.legend(["trade volume"], loc="upper right", fontsize=14)
        ax3 = plt.subplot(5, 1, 3)
        ax3.plot(self._Dt, self._fast_dif_list, 'b-', label='Macd快均线', lw=2.0)
        ax3.plot(self._Dt, self._slow_dea_list, 'r-', label='Macd慢均线', lw=2.0)
        ax3.legend(loc=0, fontsize=14)
        ax4 = plt.subplot(5, 1, 4)
        ax4.bar(x=self._Dt, height=self._macd_column_list)
        ax4.legend(["MACD bar"], loc="upper right", fontsize=14)
        ax5 = plt.subplot(5, 1, 5)
        ax5.plot(pnl_sum, 'r-', label='收益累计线', lw=2.0)
        ax5.legend(loc="upper right", fontsize=14)
        plt.show()

    def showprofit(self):
        pass


TRY = backtrade()
bar_path = 'E:\\postgraduate_life\\1A金融\\量化\\pythonProject\\venv\\hengshenghulian_daily2.csv'
backtrade.getbar(TRY, bar_path)
TRY.strategy()
TRY.run_backtrade()
profit_orders = 0
loss_orders = 0
orders = TRY._history_orders
for key in orders.keys():
    if orders[key]['pnl'] >= 0:
        profit_orders += 1
    else:
        loss_orders += 1

barx = pd.DataFrame()
barx.loc[:, 'Date'] = [date2num(x) for x in TRY._Dt[::-1]]
barx.loc[:, 'Open'] = TRY._Open[::-1]
barx.loc[:, 'High'] = TRY._High[::-1]
barx.loc[:, 'Low'] = TRY._Low[::-1]
barx.loc[:, 'Close'] = TRY._Close[::-1]
barx.loc[:, 'Volume'] = 0
fig, ax = plt.subplots()
candlestick_ohlc(
    ax,
    barx.values,
    width=0.4,
    colorup='r',
    colordown='darkgreen'
    )
# ax.xaxis_date()