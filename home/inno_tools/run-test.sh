#!/bin/sh

killall innominer_T2
killall innominer_T2
killall innominer_T2
sleep 3

pll=$1
vid=$2

innominer_T2 -o stratum+tcp://ltc-sz-factory.s.innomining.com:1800 -u inno.111 -p x --A1Pll1 $pll --A1Pll2 $pll --A1Pll3 $pll --A1Pll4 $pll --A1Pll5 $pll --A1Pll6 $pll --A1Vol $vid --api-listen >/dev/null 2>&1 &

