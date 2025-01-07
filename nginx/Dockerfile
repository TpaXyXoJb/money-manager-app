FROM python:3.9.4-slim AS server

WORKDIR /server

COPY ./server /server

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --without dev --no-root


RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.19.2

RUN rm -v /etc/nginx/nginx.conf
ADD ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
