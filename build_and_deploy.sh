#!/bin/bash

# Configuration
PROJECT_ID="agent-starter-pack-456401"
REGION="us-central1"
REPOSITORY="ai-agents"

# List of services and their respective Dockerfile paths
declare -A SERVICES
SERVICES=(
  ["content-builder"]="agents/content_builder/Dockerfile"
  ["judge"]="agents/judge/Dockerfile"
  ["orchestrator"]="agents/orchestrator/Dockerfile"
  ["researcher"]="agents/researcher/Dockerfile"
  ["course-creator"]="agents/course_creator/Dockerfile"
)

for SERVICE in "${!SERVICES[@]}"; do
  DOCKERFILE=${SERVICES[$SERVICE]}
  IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${SERVICE}:latest"

  echo "--------------------------------------------------------"
  echo "Building $SERVICE using Cloud Build..."
  echo "Dockerfile: $DOCKERFILE"
  echo "--------------------------------------------------------"

  # Submit the build to Google Cloud Build
  # Removed --tag as it conflicts with --config
  gcloud builds submit . \
    --config <(echo "
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', '$IMAGE_TAG', '-f', '$DOCKERFILE', '.']
images:
- '$IMAGE_TAG'
")

  if [ $? -eq 0 ]; then
    echo "Successfully built $SERVICE. Deploying to Cloud Run..."
    
    # Deploy to Cloud Run
    gcloud run deploy $SERVICE \
      --image $IMAGE_TAG \
      --region $REGION \
      --allow-unauthenticated \
      --port 8080
  else
    echo "Build failed for $SERVICE. Skipping deployment."
  fi
done
