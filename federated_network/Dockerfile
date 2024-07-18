# Import a large image that has all we need for building the app included
FROM python:3.11 AS builder

WORKDIR /app

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Ccopy the dependency files
COPY poetry.lock pyproject.toml ./

# Tell poetry to use a local venv
RUN $HOME/.local/bin/poetry config virtualenvs.in-project true
# Install dependencies but skip dev ones
RUN $HOME/.local/bin/poetry install --no-interaction --no-ansi

# Our service doesn't need a full OS to work, so we can use a smaller image
FROM python:3.11 AS runner

# Create a directory for our app
WORKDIR /app

# Copy the dependencies we got in the large image
COPY --from=builder /app/.venv /app/.venv
# Activate the venv
ENV PATH="/app/.venv/bin:$PATH"

# Generate the prisma client
COPY ./governance_ui/db/schema.prisma ./governance_ui/db/schema.prisma
RUN prisma generate --schema=./governance_ui/db/schema.prisma

# Copy our code
COPY ./governance_ui ./governance_ui

# Tell docker to run shiny when the image boots
CMD uvicorn governance_ui.app:app --host 0.0.0.0
