import pandas as pd
import backtrader as bt
import datetime


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close

            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than the previous close

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000)
    
    Bdata= bt.feeds.GenericCSVData(
    
        dataname='hdfc1.csv',

        fromdate=datetime.datetime(2010, 3, 11),
        todate=datetime.datetime(2020, 2, 2),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),

        datetime=2,
        high=4,
        low=5,
        open=3,
        close=6,
        volume=7,
    )
    cerebro.adddata(Bdata)
    cerebro.addstrategy(TestStrategy)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
    