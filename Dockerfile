FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

COPY . .

RUN chmod +x ./scripts/run_app.sh

EXPOSE 8000

ENV PYTHONPATH=.

CMD [ "./scripts/run_app.sh" ]