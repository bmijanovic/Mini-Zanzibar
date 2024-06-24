#!/bin/sh

# Start Consul agent in the background
consul agent -dev -client 0.0.0.0 &

# Wait for Consul to be ready
until consul info; do
  sleep 1
done

# Import key-value data
consul kv import @/consul/init_kv.json

# Keep the foreground process running
tail -f /dev/null

