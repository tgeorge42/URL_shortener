FROM python:3.10-slim

WORKDIR /app

# Copy the file for the dependencies
COPY requirements.txt ./


# Make sure the script to migrate the db and launch the project is executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files in the container
COPY . ./

# Expose the app port
EXPOSE 8000

# Launch the script
ENTRYPOINT ["/entrypoint.sh"]
