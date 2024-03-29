FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y cmake

WORKDIR /
COPY ./requirements.txt .

RUN pip install --upgrade -r ./requirements.txt

COPY ./backend /backend
COPY ./frontend /frontend
COPY ./img /img
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "80"]