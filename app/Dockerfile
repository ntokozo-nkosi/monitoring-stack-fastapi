FROM python:3.12-slim

WORKDIR /app

# install uv
RUN pip install uv

# add uv to path
ENV PATH="/root/.local/bin:${PATH}"

# copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock requirements.txt ./

# install dependencies
RUN uv sync && uv pip install -r requirements.txt

# copy the rest of the application
COPY ./app .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]