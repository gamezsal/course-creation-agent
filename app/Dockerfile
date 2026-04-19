FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy requirements from root and app code from the app directory
# This works because the build context is the repository root
WORKDIR /app
COPY requirements.txt adk_app.py ./
COPY app/ /app/

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1

# Prepare virtual environment path and ensure it's used
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

# Run the application
# Using shell form (no brackets) ensures $PORT is expanded correctly.
# Ensure main.py is configured to listen on 0.0.0.0 and the value of $PORT.
CMD python3 main.py
