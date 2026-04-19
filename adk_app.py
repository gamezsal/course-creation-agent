import sys
import os
from fastapi import FastAPI, Request
from slowapi.extension import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

# Define a key function to identify unique users (e.g., by IP)
def get_remote_address(request: Request):
    return request.client.host

# Initialize the Limiter.
# To apply to "all agents", we use the default_limits parameter.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "100 per day"]
)

app = FastAPI()

# Fix: Register the limiter and handler correctly for modern slowapi
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add the middleware to enable auto-checking for all routes (agents)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
async def root():
    # Simple health check for Cloud Run
    return {"status": "alive"}

@app.get("/agent/alpha")
async def agent_alpha(request: Request):
    return {"agent": "Alpha", "status": "Ready"}

@app.get("/agent/beta")
@limiter.limit("5 per minute", override_defaults=False)  # Apply beta-specific limit AND keep global limits
async def agent_beta(request: Request):
    return {"agent": "Beta", "status": "Busy"}

if __name__ == "__main__":
    import uvicorn
    # Simple logic to handle --host and --port if passed by Docker CMD
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8080))
    
    if "--host" in sys.argv:
        host = sys.argv[sys.argv.index("--host") + 1]
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
        
    uvicorn.run("adk_app:app", host=host, port=port, reload=False)