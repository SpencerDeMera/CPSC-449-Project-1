foreman start -m userAPI=1,postAPI=3 -p 8000

#starting hyproxy
systemctl restart haproxy
systemctl status haproxy