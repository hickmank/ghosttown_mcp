# ------------------------------------------------------------------------------
# Dockerfile for ghosttown_mcp MCP server
# This builds a minimal container with:
#  - Python 3.11 slim base image
#  - Your package installed in editable mode via flit
#  - Uvicorn to serve the FastAPI/JSON-RPC app
# ------------------------------------------------------------------------------

# 1. Use the official, slim Python 3.11 image as the base.
#    - “slim” strips out extra packages, keeping the image size small.
FROM python:3.11-slim

# 2. Set /app as the working directory for all subsequent commands.
#    - Any RUN, COPY, CMD, etc., will be relative to /app.
WORKDIR /app

# 3. Copy only the pyproject.toml first.
#    - This allows Docker to cache the dependency-install layer. If dependencies
#      don’t change, Docker will reuse this layer and speed up rebuilds.
COPY pyproject.toml .

# 4. Install Flit (the build/backend tool) and then use it to install:
#      a) Your package and its runtime dependencies (--deps production)
#      b) In editable/symlink mode so code changes reflect immediately
#    - --no-cache-dir prevents pip from keeping a local cache, reducing image size.
RUN pip install --no-cache-dir flit && \
    flit install --deps production --symlink

# 5. Copy your source code into the image.
#    - Because you installed via --symlink, this src/ directory will be linked
#      into site‑packages, so edits here update the live code.
COPY src/ src/

# 6. Document that the container listens on port 4000.
#    - EXPOSE is informational; publishing the port at runtime still requires
#      `docker run -p HOST_PORT:4000`.
EXPOSE 4000

# 7. Define the default command:
#      Launch Uvicorn to serve the FastAPI app at host 0.0.0.0, port 4000.
#    - The notation ["executable", "arg1", "arg2"] avoids a shell and is preferred.
CMD ["uvicorn", "ghosttown_mcp.server.main:app", "--host", "0.0.0.0", "--port", "4000"]
