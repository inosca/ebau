#!/bin/bash

# we need to wait and kill the nc process, since the memcache server
# keeps the connection open

echo "flush_all" | nc localhost 11211 &  PID=$! && sleep 2 && kill $PID
