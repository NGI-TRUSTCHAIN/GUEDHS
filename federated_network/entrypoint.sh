#!/bin/sh

prisma migrate dev --schema=governance_ui/db/schema.prisma

prisma generate --schema=governance_ui/db/schema.prisma

python governance_ui/db/populate_db.py

uvicorn governance_ui.app:app --host 0.0.0.0
