# Website

## Some important notes

The latest Docker Compose uses some parsing under-the-hood that makes secrets stored in `.env` files break. So any `$$` is actually a single `$` being escaped. Annoying & something that must be documented!

## Commands

Build and start everything:
```bash
sudo -E docker compose -f docker-compose.prod.yml up -d --build
```

Stop all services:
```bash
sudo -E docker compose -f docker-compose.prod.yml down
```

Export updated `requirements.txt`, necessary whenever dependencies changed:
```bash
poetry export -f requirements.txt --output requirements.txt
```

Redeploy Django app:
```bash
sudo -E docker compose -f docker-compose.prod.yml up -d --force-recreate --build web
```

### Manual management commands
```bash
sudo -E docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

```bash
sudo -E docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```

### Copying config files
Retrieve from server:
```bash
scp -r princeton@princetonpy.org:/home/princeton/princetonpy.org/prod/{.env.prod.web,.env.prod.aws,.env.prod.db,.env.prod.nginx,.env.prod.proxy-companion} .
```

Transfer to server:
```bash
scp -r $(pwd)/{.env.prod.web,.env.prod.aws,.env.prod.db,.env.prod.nginx,.env.prod.proxy-companion} princeton@princetonpy.org:/home/princeton/princetonpy.org/prod
scp -r $(pwd)/{.env.staging.aws,.env.staging.db,.env.staging.nginx,.env.staging.web,.env.staging.proxy-companion} princeton@princetonpy.org:/home/princeton/princetonpy.org/staging
```

### Importing users from CSV
Make sure file is copied to mounted app directory:
```bash
scp -r princetonpy_subscriptions.csv user@host:/path
sudo -E docker compose -f docker-compose.prod.yml run web sh
python manage.py subscriptions import ./princetonpy_subscriptions.csv
```

### Access DB
```bash
sudo -E docker compose -f docker-compose.prod.yml exec db psql -U postgres -W princetonpy_prod
# select * from django_site;
```

### Working with backup files
```bash
sudo -E docker compose -f docker-compose.prod.yml run cron ls -la /prod_backup/subscribers
sudo docker container ls
# get hash from CONTAINER ID column
sudo docker cp fc95ab44a580:/prod_backup .
```

### Manual Django shell updates

In server:
```bash
sudo -E docker compose -f docker-compose.prod.yml run web sh
```

In container:
```bash
python manage.py shell
```

And then in Django shell:
```python
import dateutil
from datetime import datetime

from meetings.models import Meeting

delta = dateutil.relativedelta.relativedelta(months=2)
before_date = datetime.now(tz=dateutil.tz.gettz("America/New_York")) - delta

# returns queryset
meeting_qs = Meeting.objects.filter(date__lte=before_date)
meeting_qs.update(tba=False)
```

### Backup DB

```bash
docker compose exec -t db pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

Use this one:
```bash
docker compose exec -t db pg_dump -U postgres princetonpy_prod > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
```

#### To restore
Rename `dump[...].sql`.

May have to manually rename `princetonpy_prod` to `princetonpy`:
```bash
cat dump_27-11-2022_16_28_02.sql | psql -U postgres -d princetonpy
```
