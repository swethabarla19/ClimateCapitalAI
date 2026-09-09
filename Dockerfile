FROM node:22.23.2-bookworm-slim AS frontend-build

WORKDIR /build/frontend
RUN npm install --global npm@11.19.1 \
    && test "$(node --version)" = "v22.23.2" \
    && test "$(npm --version)" = "11.19.1"
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/index.html frontend/tsconfig.json frontend/tsconfig.app.json frontend/tsconfig.node.json ./
COPY frontend/vite.config.ts ./
COPY frontend/public ./public
COPY frontend/src ./src
RUN npm run build

FROM python:3.14.7-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend \
    ENVIRONMENT_LABEL=production

WORKDIR /app
COPY requirements-application.txt ./
RUN python -m pip install --no-cache-dir --requirement requirements-application.txt \
    && groupadd --system --gid 10001 climatecapital \
    && useradd --system --uid 10001 --gid climatecapital --home-dir /nonexistent climatecapital

COPY backend ./backend
COPY data/governed/cross_category/runtime_v3 ./data/governed/cross_category/runtime_v3
COPY --from=frontend-build /build/frontend/dist ./frontend/dist

USER 10001:10001
EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn climatecapital.main:app --host 0.0.0.0 --port \"${PORT:-8080}\" --workers 1"]
