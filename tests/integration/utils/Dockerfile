FROM fetchai/fetchd:0.10.0

EXPOSE 26657
EXPOSE 1317
EXPOSE 9090

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]