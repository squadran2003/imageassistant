FROM nginx:1.25

USER root
RUN apt-get update

RUN apt-get install -y --no-install-recommends certbot python3-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
