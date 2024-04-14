# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm as builder

# Set the working directory in the builder stage
WORKDIR /build

# Copy the requirements file into the builder image
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN <<EOF
python3 -m venv --copies --upgrade-deps /venv
. /venv/bin/activate
pip3 install --no-cache-dir -r requirements.txt
EOF

# Start a new stage for the final image
FROM python:3.12-slim-bookworm

# Set SVC_PORT build ARg
ARG SVC_PORT=8000

ENV PATH="/venv/bin:$PATH" \
    SVC_PORT=${SVC_PORT}

# Set the working directory in the final image
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /venv /venv

# Copy the rest of the code
COPY /app/ .

# Make SVC_PORT available to the world outside this container
EXPOSE ${SVC_PORT}

# Run the application when the container launches
CMD ["python3", "app.py"]