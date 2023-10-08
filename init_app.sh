docker-compose up -d
docker exec -it mysql mysql -uroot -pROOT Cosateca < populate_database_servidor_final.sql
docker exec -it django python manage.py makemigrations
docker exec -it django python manage.py migrate