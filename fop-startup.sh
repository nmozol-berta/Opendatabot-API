#!/bin/bash


(wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip && unzip -o ovpn.zip && rm ovpn.zip) > /dev/null 2>&1
for f in ./ovpn_udp/*; do 
    echo 'route 10.0.15.0 255.255.255.0 net_gateway' >> $f 
    echo 'route 10.0.0.0 255.255.255.0 net_gateway' >> $f  
    echo 'route 10.0.101.0 255.255.255.0 net_gateway' >> $f
    echo 'route 10.0.100.0 255.255.255.0 net_gateway' >> $f
#    echo 'route 172.22.0.0 255.255.255.0 net_gateway' >> $f
done
#openvpn --config ovpn_udp/ua${VPN_CODE}.nordvpn.com.udp.ovpn --auth-user-pass temp_cred.txt &
sleep 5
#echo 'nameserver 8.8.8.8' > /etc/resolv.conf

if ! ping -c 4 google.com &> /dev/null; then
 echo "ERROR: No internet connection. Shutting down container." >&2
 exit 1  
else
 echo "OK: Internet connection exists."
fi


python ./app_fop.py

