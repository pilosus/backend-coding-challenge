# We don't need to build anything with GNU/libc, so let's stick to a small Apline base image
FROM python:3.11-alpine
EXPOSE 9876
ENV PYTHONPATH=/usr/src/app
WORKDIR /usr/src/app
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .
COPY . .

CMD ["python", "/usr/src/app/gistapi/app.py"]
