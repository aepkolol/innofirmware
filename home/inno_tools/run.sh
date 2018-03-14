#!/bin/sh

pll=$1
vid=$2

# 看算力
#https://btc.innomining.com/
#https://ltc.innomining.com/

# inno池
# A5
#cgminer -o stratum+tcp://btc.s.innomining.com:1800 -u inno.111 -p x --A1Pll1 $pll --A1Pll2 $pll --A1Pll3 $pll --A1Pll4 $pll --A1Pll5 $pll --A1Pll6 $pll --A1Vol $vid --api-listen
# A6
cgminer -o stratum+tcp://ltc.s.innomining.com:1900 -u inno.111 -p x --A1Pll1 $pll --A1Pll2 $pll --A1Pll3 $pll --A1Pll4 $pll --A1Pll5 $pll --A1Pll6 $pll --A1Vol $vid --api-listen
# A7
#cpuminer -a X11 -o stratum+tcp://dash.s.innomining.com:2000 -u inno.1111 -p x -t 1
#sgminer -o stratum+tcp://dash.s.innomining.com:2000 -u inno.1111 -p x --api-listen


# 鱼池
# A5
#cgminer -o stratum+tcp://stratum.f2pool.com:3333 -u inno.111 -p x --A1Pll1 $pll --A1Pll2 $pll --A1Pll3 $pll --A1Pll4 $pll --A1Pll5 $pll --A1Pll6 $pll --A1Vol $vid --api-listen
# A6 
#cgminer -o stratum+tcp://stratum.f2pool.com:8888 -u inno.111 -p x --A1Pll1 $pll --A1Pll2 $pll --A1Pll3 $pll --A1Pll4 $pll --A1Pll5 $pll --A1Pll6 $pll --A1Vol $vid --api-listen
# A7 第三方
#cpuminer -a X11 -o stratum+tcp://x11gz.ltc1btc.com:3333 -u inno_x11.01 -p x -t 1
#sgminer -o stratum+tcp://x11gz.ltc1btc.com:3333 -u inno_x11.01 -p x --api-listen

