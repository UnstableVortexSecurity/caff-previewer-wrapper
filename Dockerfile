FROM python:3.8-alpine
COPY --from=registry.kmlabz.com/unstablevortex/caff-previewer:latest /usr/local/bin/caff_previewer /usr/local/bin/caff_previewer

WORKDIR /app

ARG RELEASE_ID
ENV RELEASE_ID ${RELEASE_ID:-""}

COPY requirements.txt ./

RUN apk update && apk add imagemagick && pip3 install --no-cache-dir -r requirements.txt && rm -f requirements.txt && adduser -D -H -s /bin/false -u 1000 caffsvc

COPY ./caff_previewer_wrapper .

EXPOSE 8080

USER 1000
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "app:app"]