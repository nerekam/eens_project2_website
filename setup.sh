mkdir -p certs
mkdir -p log
mkdir -p data

echo "Creating self-signed certificate. (Not best practice in real-life, but will suffice for this homework.)"
echo "=================================================================================================="
sudo openssl req -x509 -newkey rsa:4096 -keyout certs/key.key -out certs/cert.crt -days 365 -nodes -subj "/C=TW/ST=Tainan/L=Tainan/O=EENS project 2/OU=Team Apple/CN=EENS project 2 Team Apple"

# Setting permission for certs
sudo chown root:root certs
sudo chmod 0600 certs

echo "Building and starting docker containers."
echo "=================================================================================================="
sudo docker-compose build

sudo docker-compose up -d

sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin', 'admin')"
sudo docker-compose exec web python manage.py loaddata initial_data

sudo docker-compose exec web-insecure python manage.py migrate
sudo docker-compose exec web-insecure python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin', 'admin')"
sudo docker-compose exec web-insecure python manage.py loaddata initial_data

sudo docker-compose logs -f