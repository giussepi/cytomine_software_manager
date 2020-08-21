#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    create user $POSTGRES_DB_USER with encrypted password '$POSTGRES_DB_PASS';
    create database $POSTGRES_DB_NAME;
    grant all privileges on database $POSTGRES_DB_NAME to $POSTGRES_DB_USER;
EOSQL
