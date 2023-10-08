FROM python:3.11.4
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install -r requirements.txt
RUN pip install Django==4.2.3
RUN pip install django-bootstrap4
RUN pip install mysql-connector-python
RUN pip install django-minio-backend
RUN pip install channels_redis
RUN python -m pip install -U channels[daphne]
RUN pip install pytest-django

COPY . .

EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
