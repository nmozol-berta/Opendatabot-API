docker compose up -d --build
project_name=$(basename "$(pwd)")
network_name="${project_name}_webnetwork"
subnet=$(docker network inspect "$network_name" | jq -r '.[0].IPAM.Config[0].Subnet')
sudo iptables -t nat -A POSTROUTING -s 10.0.15.0/24 -d $subnet -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -d $subnet -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -s 10.0.101.0/24 -d $subnet -j MASQUERADE
#sudo iptables -t nat -A POSTROUTING -s 10.0.100.0/24 -d $subnet -j MASQUERADE
#sudo iptables -t nat -A POSTROUTING -s 172.22.0.0/24 -d $subnet -j MASQUERADE