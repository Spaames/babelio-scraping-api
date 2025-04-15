FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Install Poetry package manager
RUN pip install --no-cache-dir poetry

# Copy only the dependency files first (to leverage Docker cache)
COPY pyproject.toml poetry.lock ./

# Configure Poetry to install dependencies directly in the container environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the Flask/Gunicorn port
EXPOSE 5000

# Run the app using Gunicorn (more suitable for production)
CMD ["poetry", "run", "gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
