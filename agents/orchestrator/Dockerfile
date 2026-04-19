FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy requirements from root and agent code from the agent directory
# This works because the build context is now the repository root
COPY requirements.txt adk_app.py ./
COPY agents/orchestrator/ .
COPY adk_app.py .

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1

# Prepare virtual environment path
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    if [ -f pyproject.toml ]; then \
        uv sync --active; \
    elif [ -f requirements.txt ]; then \
        uv pip install -U -r requirements.txt; \
    else \
        echo "Neither pyproject.toml nor requirements.txt found" && exit 1; \
    fi

# Set host and port
ENV HOST 0.0.0.0

# Run ADK API Server
# Shell form ensures $PORT is expanded correctly for Cloud Run
CMD python3 adk_app.py --host 0.0.0.0 --port $PORT --trace_to_cloud --a2a
