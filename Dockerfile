FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --frozzen --no-cache --no-dev

COPY . .

RUN chmod +x ./scripts/start_app.sh

CMD [ "./scripts/start_app.sh" ]