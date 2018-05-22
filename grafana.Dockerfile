FROM grafana/grafana:5.1.3
USER root

RUN apt-get update && apt-get install -y \
  zip \
  unzip

RUN mkdir /opt/grafana
ENV GF_PATHS_PLUGINS=/opt/grafana

COPY scripts/candle_stick_plugin.sh /opt/grafana/candle_stick_plugin.sh
RUN chmod 777 /opt/grafana/candle_stick_plugin.sh
RUN /opt/grafana/candle_stick_plugin.sh