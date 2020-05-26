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

    3. You can see the logs by running:

	   `tail -f /var/lib/postgresql/12/main /var/log/postgresql/postgresql-12-main.log`

4. Install psycopg2

   [Follow these instructions](https://www.psycopg.org/docs/install.html)

5. Create your new database, user and pass

	`sudo -u postgres createdb cyto_soft_mgr_db`
	`sudo -u postgres pqsl`
	`create user QNZhang with encrypted password 'MMVB10medical';`
	`grant all privileges on database cyto_soft_mgr_db to QNZhang;`

6. Make manage.py executable

        `sudo chmod +x manage.py`

7. Run DB migrations

	`./manage.py migrate`

8. Create your admin super user

	`./manage.py createsuperuser`

9. Install/run RabbitMQ

    `docker run -d -p 5672:5672 rabbitmq`



# DEVELOPMENT MODE

## DJANGO

1. Set debug mode in cyto_soft_mgr.config.settings.py

	`DEBUG = True`

2. Make manage.py executable (if you haven't done it before)

    `sudo chmod +x manage.py`

3. Make sure the RabbitMQ docker container is running. See step 9 from installation section

4. Run django development server

    `./manage.py runserver 0.0.0.0:8082`


## CELERY

1. Run the celery worker server (from the same folder where manage.py is located)

	`celery -A cyto_soft_mgr worker -l info`


# PRODUCTION MODE

## DJANGO

1. Run Django collectstatic command

	`./manage.py collectstatic`

2. Set `settings.DEBUG` to False

3. Add your server IP to `settings.ALLOWED_HOSTS`


## CELERY

1. Make sure the RabbitMQ docker container is running. See step 9 from installation section

2. Run Celery as a daemon
