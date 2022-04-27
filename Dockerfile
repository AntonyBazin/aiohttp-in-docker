FROM python:3.8.10
MAINTAINER Anton Bazin antonyvbazin@gmail.com
EXPOSE 8080
COPY ./ ./home/task
WORKDIR ./home/task
RUN python3 -m pip install -r requirements.txt
CMD ["bash", "start_services.sh"]
