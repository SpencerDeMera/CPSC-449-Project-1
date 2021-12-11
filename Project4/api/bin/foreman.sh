# Starting foreman
foreman start -m userAPI=1,postAPI=3,pollsAPI=1,likesAPI=1,srvRegAPI=1 -p 8100

# Starting hyproxy
systemctl restart haproxy
systemctl status haproxy

# To kill running redis: killall redis-server
