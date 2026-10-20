# Best Cars Dealership Portal

**Project:** Full Stack Application Development Capstone Project

**Developer:** Talgat Yerkhanuly Sailaubekov

**Course:** IBM Cloud Native Full Stack Development Capstone

Best Cars is a responsive dealership-review portal built with Django, React, SQLite, Docker, and GitHub Actions. Visitors can browse dealership branches, filter them by state, and read customer reviews. Registered users can log in and add a review; each submitted review receives a positive, neutral, or negative sentiment label.

## Features

- Responsive landing, About Us, Contact Us, login, registration, dealer-list, dealer-detail, and review-submission pages
- Session-based Django authentication
- Dealer search and state filtering, including Kansas
- Car make and model administration through Django Admin
- Review sentiment analysis endpoint
- Automated Django tests and React production build in GitHub Actions
- Docker-ready deployment configuration

## Technology

- Frontend: React 18 and React Router
- Backend: Django 4.2
- Data: SQLite with the IBM capstone dealership and review seed data
- Delivery: Docker, GitHub Actions, Gunicorn, and WhiteNoise

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
python server/manage.py migrate
python server/manage.py seed_capstone

cd server/frontend
npm ci
npm run build
cd ../..

python server/manage.py runserver 0.0.0.0:8000
```

Open `http://127.0.0.1:8000/`.

Demo application user:

- Username: `talgat`
- Password: `Capstone123!`

Demo Django admin user:

- Username: `root`
- Password: `RootPass123!`

These credentials belong only to the seeded demonstration database and must be replaced for a real production deployment.

## API examples

```bash
curl -s http://127.0.0.1:8000/djangoapp/get_dealers
curl -s http://127.0.0.1:8000/djangoapp/get_dealers/Kansas
curl -s http://127.0.0.1:8000/djangoapp/dealer/15
curl -s http://127.0.0.1:8000/djangoapp/reviews/dealer/15
curl -s http://127.0.0.1:8000/djangoapp/get_cars
curl -s 'http://127.0.0.1:8000/djangoapp/analyze/Fantastic%20services'
```

The submission evidence files in the repository root contain the commands and verified outputs required by the final project rubric.

## Tests

```bash
python server/manage.py test djangoapp
cd server/frontend && npm run build
```

## Container

```bash
docker build -t best-cars-capstone .
docker run --rm -p 8000:8000 best-cars-capstone
```
