FROM python:3.8

RUN apt-get -y update && apt-get install -y --no-install-recommends \
  wget \
  python3 \
  nginx \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*


COPY apps/yue-translate/src/requirements.txt /opt/program/requirements.txt
RUN pip install -r /opt/program/requirements.txt && \
  rm -rf /root/.cache

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
WORKDIR /opt/program
COPY apps/yue-translate/src /opt/program

CMD [ "serve" ]