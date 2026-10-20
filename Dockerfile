FROM node:20-alpine AS frontend
WORKDIR /app/server/frontend
COPY server/frontend/package*.json ./
RUN npm ci
COPY server/frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt
COPY server/ /app/server/
COPY --from=frontend /app/server/frontend/build /app/server/frontend/build
RUN python server/manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh", "-c", "python server/manage.py migrate --noinput && python server/manage.py seed_capstone && gunicorn --chdir server djangoproj.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
