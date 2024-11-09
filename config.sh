#!/bin/bash

echo "Configuring server info..."
if [ -f ".env" ]; then
  rm .env
  echo ".env file already existed and has been deleted."
fi

echo "Please enter the server IP address:"
read SERVER_IP
echo "Please enter the server port:"
read SERVER_PORT

echo "SERVER_IP=$SERVER_IP" > .env
echo "SERVER_PORT=$SERVER_PORT" >> .env

echo "Configuration completed."