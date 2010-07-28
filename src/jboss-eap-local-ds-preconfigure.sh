#!/bin/sh

DATABASE_NAME=eap
DATABASE_USER=eap
DATABASE_PASSWORD=eap

USER_CREATED=`/bin/su postgres -c "/bin/echo '\du' | /usr/bin/psql -tA" | awk -F\| '{ print $1 }' | grep $DATABASE_USER | wc -l`
DATABASE_CREATED=`/bin/su postgres -c "/usr/bin/psql -tAl" | awk -F\| '{ print $1 }' | grep $DATABASE_NAME | wc -l`

if [ $USER_CREATED -eq "0" ]
then
    /bin/su postgres -c "/usr/bin/createuser -SDR $DATABASE_USER"
fi

echo "ALTER USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASSWORD';" | /bin/su postgres -c /usr/bin/psql > /dev/null

if [ $DATABASE_CREATED -eq "0" ]
then
    /bin/su postgres -c "/usr/bin/createdb -O $DATABASE_USER $DATABASE_NAME"
fi