# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

# Install uv from the official binaries
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1
# Use 'copy' mode for linking since Docker file systems can be tricky
ENV UV_LINK_MODE=copy

# Copy only the dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv
# --frozen ensures we use the exact versions from uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# --- Stage 2: Runtime ---
FROM python:3.12-slim

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Add the virtual environment to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy your application code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run the application
# 0.0.0.0 is required for the app to be accessible outside the container
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]