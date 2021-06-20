from config import settings
from yoyo import read_migrations, get_backend

backend = get_backend(settings.postgres_url)
migrations = read_migrations("./migrations/scripts")
with backend.lock():
	backend.apply_migrations(backend.to_apply(migrations))
