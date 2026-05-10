# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Install system dependencies required for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --user -r requirements.txt || \
    (pip install --no-cache-dir --user --upgrade pip && pip install --no-cache-dir --user -r requirements.txt)

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_INPUT=1

# Copy application code
COPY . .

# Create static and media directories
RUN mkdir -p /app/staticfiles /app/media

# Expose port
EXPOSE 8000

# Collect static files and run migrations
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:8000 --workers 4"]
