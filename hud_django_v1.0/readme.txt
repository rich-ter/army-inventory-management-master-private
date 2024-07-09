to run the server in the current directory do:

docker-compose up --build

if you change the server IP make sure you adjust the nginx.conf 

server_name localhost;  # Replace with your domain or IP address

in order to run you need to have downloaded the offline image and then load it for

nginx,
python3.10

In order to create the data from baseline

python manage.py create_all_data

CAREFUL! THIS WILL DELETE ALL PREVIOUS ENTRIES.

---

IN ORDER TO RUN FROM SCRATCH:

- LOAD DOCKER AND NGINX image
- SET NGINX WITH THE SERVER IP 
