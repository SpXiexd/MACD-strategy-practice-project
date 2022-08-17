# MACD-strategy-practice-project
Based on a bilibili videos tutorial of building a MA20 trading strategy,trying to practice skill of buiding MACD simple strategy.So it is just a very simple code.
#------------------------------------------------------------------------------------#
##<getdata>
Before running code <quant2>,you should run <getdata> first to get history data from jquant community:1.Sign up an account of jquant community.2.Getting the code of a stock 
or an ETF you like.3.Specifying path you want to store the data.
##<quant2>
It is about calculate MACD of an ETF,and support we only have 10000yuan,and have limit of only one order.When fast line(dif) bigger than slow line(dea)，if there is no buy order exits,then execute buy order.
When fast line(dif) smaller than slow line(dea)，if there is buy order exits,then execute sale order.
There is also an dictionary record every order.And,the code can also plot cumulative profit,MACD curve,and candle curve.
Unfortunatly,the strategy behave really bad ,hhh.
