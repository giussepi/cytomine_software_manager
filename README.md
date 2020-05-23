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



# RUN DJANGO DEVELOPMENT SERVER

1. Make manage.py executable (if you haven't done it before)

    `sudo chmod +x manage.py`

2. Run django server

    `./manage.py runserver 0.0.0.0:8082`
