#!/usr/bin/sh

# Extracting ZFS name:

output=$(/TopStor/etcdget.py 10.11.11.100 mynode --prefix)

mynode_name=$(echo "$output" | grep -oP "(?<=\('mynode', ')\S+(?='\))")
mynode_ip=$(echo "$output" | grep -oP "(?<=\('mynodeip', ')\S+(?='\))")

echo "Node Name: $mynode_name"
echo "Node IP: $mynode_ip"
#---------------------------------------------------------------------------------

# Searching through the database etherports/$mynode_name (ZFS name) and saving all saved ports in result
result=$(/TopStor/etcdget.py 10.11.11.100 "etherports/$mynode_name" --prefix)
echo "etcd.get: $result"
#---------------------------------------------------------------------------------

# Get network interfaces
pports=$(ip a | awk -F: '/^[0-9]+: / {print $2}' | tr -d ' ')

# Loop through each interface and extract IP addresses
for port in $pports; do
    # Extract IP addresses for the current interface
    ip_address=$(ip a show "$port" 2>/dev/null | grep -oP '(?<=inet\s)\d+\.\d+\.\d+\.\d+')

    # Proceed only if the interface has an IP address
    if [ -n "$ip_address" ]; then
        echo "Interface: $port"
        echo "IP addresses for $port:"
        echo "$ip_address"

        # Check if the port and IP are already in the etcd database
        if echo "$result" | grep -q "etherports/$mynode_name/$port'"; then
            echo "Port $port with IP $ip_address is already in the database, skipping etcdput."
        else
            # Update etcd with the interface and its IP address
            /TopStor/etcdput.py 10.11.11.100 "etherports/$mynode_name/$port" "$ip_address"
            echo "Updated etcd with port $port and IP $ip_address."
        fi

        echo
    fi
done
