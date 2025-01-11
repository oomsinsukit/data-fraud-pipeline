#!/bin/bash

set -e

# Install requirements if requirements.txt exists
if [ -e "/opt/airflow/requirements.txt" ]; then
  echo "Installing Python requirements..."
  pip install --no-cache-dir -r /opt/airflow/requirements.txt
fi

# Apply any database migrations (initializes the database if not already initialized)
echo "Upgrading Airflow database..."
airflow db upgrade

# Create the admin user if it doesn't already exist
if ! airflow users list | grep -qw 'admin'; then
  echo "Creating admin user..."
  airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
else
  echo "Admin user already exists. Skipping user creation."
fi

# Start the Airflow webserver
echo "Starting Airflow webserver..."
exec airflow webserver