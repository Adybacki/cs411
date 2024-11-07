#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


##########################################################
#
# Meal Management
#
##########################################################

# Add meal
create_meal() {
  meal_name=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Adding meal ($meal_name, Cuisine: $cuisine) to the kitchen..."
  response=$(curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal_name\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}")
  
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal."
    echo "Response from server: $response"  # Print response for debugging
    exit 1
  fi
}

# Delete meal by ID
delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    echo "Response from server: $response"
    exit 1
  fi
}

# Get all meals
get_all_meals() {
  echo "Getting all meals in the kitchen..."
  response=$(curl -s -X GET "$BASE_URL/meals")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All meals retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meals JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meals."
    echo "Response from server: $response"
    exit 1
  fi
}


# Get meal by ID
get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    echo "Response from server: $response"
    exit 1
  fi
}



############################################################
#
# Battle Management
#
############################################################

prepare_meals_for_battle() {
  meal1_id=$1
  meal2_id=$2

  echo "Preparing meals $meal1_id and $meal2_id for battle..."
  response=$(curl -s -X POST "$BASE_URL/battle/prepare" -H "Content-Type: application/json" \
    -d "{\"meal1_id\": $meal1_id, \"meal2_id\": $meal2_id}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meals prepared for battle successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Battle Preparation JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to prepare meals for battle."
    exit 1
  fi
}

start_battle() {
  battle_id=$1

  echo "Starting battle ID ($battle_id)..."
  response=$(curl -s -X POST "$BASE_URL/battle/start/$battle_id")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Battle started successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Battle JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to start battle."
    exit 1
  fi
}

get_leaderboard() {
  echo "Retrieving leaderboard..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve leaderboard."
    exit 1
  fi
}


# Health checks
check_health
check_db

# Meal Management Tests
create_meal "Spaghetti" "Italian" 10.99 "MED"
create_meal "Sushi" "Japanese" 12.99 "LOW"
create_meal "Burger" "American" 8.99 "HIGH"

delete_meal_by_id 1
get_all_meals

get_meal_by_id 2

# Battle Management Tests
prepare_meals_for_battle 2 3
start_battle 1

# Leaderboard
get_leaderboard

echo "All tests passed successfully!"
