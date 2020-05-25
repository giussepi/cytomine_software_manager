# cytomine_software_manager
Interface to run cytomine software that requires GPU


# INSTALLATION
1. Create a virtual environment (optional)

2. Install requirements

   `pip install -r requirements.txt`

3. Install PostgreSQL
    1. [Follow these instructions](https://www.postgresql.org/download/linux/ubuntu/)
    2. You can now start the database server using:

  	   `pg_ctlcluster 12 main start`

    2. You can see the logs by running:

	   `tail -f /var/lib/postgresql/12/main /var/log/postgresql/postgresql-12-main.log`

4. Install psycopg2

   [Follow these instructions](https://www.psycopg.org/docs/install.html)

5. Create your new database, user and pass

	`sudo -u postgres pqsl`
	`createdb cyto_soft_mgr_db;`
	`create user QNZhang with encrypted password 'MMVB10medical';`
	`grant all privileges on database cyto_soft_mgr_db to QNZhang;`

6. Run DB migrations

	`./manage.py migrate`

7. Create your admin super user

	`./manage.py createsuperuser`

8. Install/run RabbitMQ
    `docker run -d -p 5672:5672 rabbitmq`



# DEVELOPMENT MODE

## RUN DJANGO DEVELOPMENT SERVER

1. Set debug mode in cyto_soft_mgr.config.settings.py

	`DEBUG = True`

2. Make manage.py executable (if you haven't done it before)

    `sudo chmod +x manage.py`

3. Run django server

    `./manage.py runserver 0.0.0.0:8082`


## RUN CELERY WORKER

1. Run the celery worker server (from the same folder where manage.py is located)

	`celery -A cyto_soft_mgr worker -l info`
