FROM postgres
MAINTAINER Anton Bazin antonyvbazin@gmail.com
EXPOSE 5432
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ADD create.sql /docker-entrypoint-initdb.d
