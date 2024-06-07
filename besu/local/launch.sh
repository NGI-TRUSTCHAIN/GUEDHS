#!/bin/bash

# Build Docker image
docker build . -t my-besu:latest

# Launch Docker Compose
docker-compose up -d
