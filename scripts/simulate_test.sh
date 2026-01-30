#!/bin/bash
echo "🧹 Cleaning up existing containers..."
docker-compose down -v

echo "🚀 Starting OrderMesh System..."
docker-compose up --build -d

echo "⏳ Waiting for system to warm up (30s)..."
sleep 30

echo "📊 Current Analytics Metrics:"
docker-compose logs analytics | tail -n 5

echo "🧪 Simulating Consumer Failure (Stopping Inventory Service)..."
docker-compose stop inventory
sleep 10
echo "📈 Checking Analytics during failure (Production should continue)..."
docker-compose logs analytics | tail -n 5

echo "🔄 Restarting Inventory Service..."
docker-compose start inventory
sleep 10

echo "🔍 Checking for DLQ alerts..."
docker-compose logs dlq-logger | grep "DLQ ALERT" | tail -n 5

echo "🏁 Simulation complete. Check logs for performance metrics."
