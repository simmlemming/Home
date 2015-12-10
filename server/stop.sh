#!/bin/bash

echo "Stopping..."
pkill --signal 15 -f 'python3.4 -m org.home.server.home'
if [ $? -eq 0 ]
then
    echo "Server stoped."
else
    echo "Server NOT stoped."
fi