FROM alpine 

RUN apk add --no-cache python3-dev gcc && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir --upgrade pip && \
    apk --update add --no-cache build-base && \
    apk add --no-cache mariadb-dev && \
    apk add --no-cache mysql-dev && \
    apk add linux-headers

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

CMD ["python3","Process_Globant/Challenge1_R2.ipynb","Process_Globant/Challenge2_R1.ipynb"]

