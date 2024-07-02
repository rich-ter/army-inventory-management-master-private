# WAREHOUSE MANAGEMENT SYSTEM

![](https://raw.githubusercontent.com/rich-ter/army-inventory-management/master/github_images/1920x1080.jpg)




[![Latest Commit](https://img.shields.io/github/last-commit/rich-ter/army-inventory-management)](https://github.com/rich-ter/army-inventory-management/commits/main)
## Tech stack
- Back-end: 
![](https://img.shields.io/badge/Code-Python-informational?style=flat&logo=Python&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Code-Django-informational?style=flat&logo=Django&logoColor=white&color=4AB197) <br>
- Front-end:
![](https://img.shields.io/badge/Code-Bootstrap-informational?style=flat&logo=Bootstrap&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Code-JavaScript-informational?style=flat&logo=JavaScript&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Code-Docker-informational?style=flat&logo=Docker&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Code-Nginx-informational?style=flat&logo=Nginx&logoColor=white&color=4AB197)
![](https://img.shields.io/badge/Code-Gunicorn-informational?style=flat&logo=Gunicorn&logoColor=white&color=4AB197)

## Table of contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

# Introduction


Welcome to the Warehouse Management System (WMS) project! This system is designed to streamline and optimize military warehouse operations by providing efficient management of inventory, orders, and logistics.




![](https://raw.githubusercontent.com/rich-ter/army-inventory-management/master/github_images/db_scheme_V3.png)

![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=rich-ter&repo=army-inventory-management&theme=dark&layout=compact)



## Features


- Inventory Management: Track and manage stock levels, product locations, and inventory movements.
- Order Management: Handle order processing, fulfillment, and shipment tracking.
- Reporting and Analytics: Generate reports on inventory levels, order status, and performance metrics.
- User Management: Define roles and permissions for different users within the system.
- Integration: Seamlessly integrate with other military systems. 
- Print military protocol

## Installation (Django)



1.Give the following command to open the virtual environment and activate the system

    . venv/Scripts/activate 

2.After installing Django, follow the next steps to modify the system 📦:

-Copy the project warehouses 🐙.

-Modify the database settings 'settings.py'.

-Complete the immigration to create the necessary database. 

    python manage.py makemigrations
    python manage.py migrate

3.Create an admin user with access to the admin hub in Django

    python manage.py createsuperuser

4.Run the server 🏃: 

    python manage.py runserver

The above process will start the server development in Django on your local computer and will include a URL (ex. http://127.0.0.1:8000/), therefore allowing you to open the website on your browser.

### Prerequisites
Make sure your computer meet the following requirements:

1.Python: Your system requires Python for Django to run.

2.Django: After installing Python to your systen, you can install Django using the pip command


## Usage

There are three main user, the two of them have access to their own sector domains and the third one is an admin with access to all the available data.

Once the system is up and running, you can perform the following actions:

- Add Products: Add new products to the inventory.
- Manage Stock: Update stock levels and track military equipment inventory movements.
- Process Orders: Create and manage military bases' orders, and update their fulfillment status.
- Generate Reports: View and export reports on various warehouse metrics.


<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXy4gTMb9AtJU6L-RCPYC8WMWkJ8cjrVEWtg&s" width="300" height="225"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/HellenicArmySeal.svg/1200px-HellenicArmySeal.svg.png" width="230" height="230">
```bash


