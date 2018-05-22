#!/bin/sh

cd /opt/grafana
curl -LOs https://github.com/ilgizar/ilgizar-candlestick-panel/raw/master/pack/ilgizar-candlestick-panel.zip > ilgizar-candlestick-panel.zip && \
unzip ilgizar-candlestick-panel.zip && \
rm ilgizar-candlestick-panel.zip