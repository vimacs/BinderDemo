#!/bin/bash
# Build script for Render deployment
# This runs on EVERY deploy

set -e

echo "🔨 Building Binder Backend..."

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run ALL migrations (creates tables if missing)
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Create default permissions (idempotent)
echo "🔑 Setting up permissions..."
python manage.py create_default_permissions || true

# Seed admin accounts (idempotent — skips existing)
echo "👤 Seeding admin accounts..."
python manage.py seed_admins

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete!"
