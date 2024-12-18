#!/bin/sh

prisma migrate deploy --schema=governance_ui/db/schema.prisma

prisma generate --schema=governance_ui/db/schema.prisma

PYTHONPATH=. python governance_ui/db/populate_db.py

uvicorn governance_ui.app:app --host 0.0.0.0
