set -e

host="$1"
shift

until PGPASSWORD='req_passwd' psql -h "$host" -d "requeststask" -U "req_user" -c '\q'; do
  >&2 echo "Postgres database is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres database is up - proceeding"
exec "$@"