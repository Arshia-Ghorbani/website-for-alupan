FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/alupan.conf /etc/nginx/conf.d/alupan.conf
COPY docker/nginx/proxy_params.conf /etc/nginx/proxy_params.conf

RUN mkdir -p /var/www/static /var/www/media

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -qO- http://localhost/health/live/ || exit 1
