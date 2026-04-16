# Seth Sanwara Luxury Shop

A luxury jewelry shop website built with Django, featuring live metal prices and a stunning user interface.

## Project Features
- **Modern Django Stack**: Built using Django 6.x.
- **Live Metal Pricing**: Integrated with Metals.dev to display accurate market rates for gold and silver.
- **Dynamic Theming**: Admin-configurable themes for seamless branding updates.
- **Secure Handling**: Utilizes Python environments and `dj-database-url` for secure configuration management.

## Prerequisites
- Python 3.9+
- MySQL (or PostgreSQL/SQLite based on your preference)
- Metals.dev API Key (for live prices)

## Local Setup

**1. Clone the repository and enter the directory**
```bash
git clone <your-github-repo-url>
cd "shop website"
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Copy the `.env.example` file to create your own local `.env`:
```bash
cp .env.example .env
```
Ensure you update the `DATABASE_URL` in `.env` to match your local MySQL configuration, for example:
`DATABASE_URL=mysql://root:password@127.0.0.1:3306/seth_sanwara_db`

**4. Run Migrations and Start the Server**
```bash
python manage.py migrate
python manage.py runserver
```

## Deployment to Vercel

If you aim to deploy this application to Vercel, keep in mind:
- **Serverless PostgreSQL**: Vercel does not support persistent local MySQL/SQLite databases since instances are ephemeral. You must use an external database provider like Vercel Postgres, Supabase, or PlanetScale.
- **Environment Variables**: Add your `DATABASE_URL`, `SECRET_KEY`, `ALLOWED_HOSTS` and any other secrets via the Vercel dashboard.
- **Static Files**: The project is structured with `whitenoise` to serve static files. `vercel.json` routes the requests to the WSGI application properly.

To deploy via the Vercel CLI:
```bash
npm i -g vercel
vercel deploy
```
Or simply connect your GitHub repository in the Vercel Dashboard!

## Scripts
Any setup / seeding scripts (such as `seed_db.py`, `theme_setup.py`) can be found within the `scripts/` directory.

```bash
python scripts/seed_db.py
```
