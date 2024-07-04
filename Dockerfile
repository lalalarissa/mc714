FROM python:3.11.5
RUN apt-get update && apt-get install -y mpich
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install mpi4py
CMD ["python"]
