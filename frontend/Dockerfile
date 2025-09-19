FROM nginx:alpine
COPY app /usr/share/nginx/html
# we will use an nginx config to reverse-proxy /api-proxy to backend service via k8s service URL (or use same-origin + env)
EXPOSE 80
