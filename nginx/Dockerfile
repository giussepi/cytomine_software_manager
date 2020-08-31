FROM nginx:1.19.2

# Install logrotate
RUN apt-get update && apt-get -y install logrotate

COPY start.sh /start.sh

RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]

CMD ["nginx", "-g", "daemon off;"]
