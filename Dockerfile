FROM python:3.8.10
MAINTAINER Anton Bazin antonyvbazin@gmail.com
EXPOSE 8080
ENV POSTGRES_PASSWORD password
RUN apt update
RUN apt-get -y install postgresql-client
COPY ./ ./home/task
WORKDIR ./home/task
RUN python3 -m pip install -r requirements.txt
CMD ["bash", "wait_for_postgres.sh", "db", "bash", "start_services.sh"]
