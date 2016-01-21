#!/bin/bash

echo "Stopping..."
pkill --signal 9 -f 'python3.4 -m org.home.server.home'
if [ $? -eq 0 ]
then
    echo "Server stopped."
else
    echo "Server NOT stopped."
fi