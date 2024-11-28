FROM python:3.11-rc-bullseye AS deps

WORKDIR /app
RUN apt-get update \
    && apt-get install -y gcc g++ gfortran libopenblas-dev liblapack-dev pkg-config \
    build-essential checkinstall zlib1g-dev libssl-dev cmake \
    ffmpeg libsm6 libxext6 \ 
    && rm -rf /var/lib/apt/lists/*
RUN pip install setuptools
COPY ["requirements.txt", "."]
RUN pip install -r requirements.txt

ENV VISUALIZE=false

FROM deps AS final

COPY . .

ENTRYPOINT [ "python", "main.py" ]