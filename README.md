# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our InteRacker webapp helps students to stay organized, meet deadlines, and confidently navigate the internship and job application process.

## User stories

[Issues Page](https://github.com/swe-students-spring2026/2-web-app-prism_panthers/issues)


## Steps necessary to run the software

1. **Clone the repository**
   ```bash
   git clone https://github.com/software-students-spring2026/2-web-app-prism_panthers.git
   cd 2-web-app-prism_panthers
   ```

2. **Create and activate a virtual environment**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your values:
   - `SECRET_KEY` — a random secret string
   - `MONGO_URI` — your MongoDB connection string (e.g. `mongodb://localhost:27017`)
   - `DB_NAME` — database name (default: `internship_tracker`)

5. **Start MongoDB**
   Make sure MongoDB is running locally, or use a cloud instance (e.g. MongoDB Atlas) and update `MONGO_URI` accordingly.

6. **Run the application**
   ```bash
   python3 app.py
   ```

7. **Open in browser**
   Visit [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

## Task boards
[Task board for Sprint 1](https://github.com/orgs/swe-students-spring2026/projects/4/views/1)
[Task board for Sprint 2](https://github.com/orgs/swe-students-spring2026/projects/55/views/1)
