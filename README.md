# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Our InteRacker webapp helps students to stay organized, meet deadlines, and confidently navigate the internship and job application process.

## User stories

- As a job seeker, I want to save jobs that I am interested in and log the application deadline, company, role, link to application portal, application status, application details, date applied.

- As an applicant, I want to view a summary list of all my applications/interested jobs, so I can quickly see my current progress.

- As an applicant, I want to access a detailed view of a saved job—including the description, requirements, and personal notes—so I can keep my interview preparation organized and distinct for each company.

- As a applicant, I want to update the status (e.g., from "Interested" to "Applied"), so my dashboard accurately reflects where I stand in the hiring process.

- As a user who made a mistake, I want to edit the details of an existing entry (like fixing a typo in the company name), so my data remains professional and accurate.

- As a rejected or uninterested candidate, I want to delete or archive an application from my list, so I can focused only on active opportunities.

- As an applicant with multiple applications, I want to search for a company by name, so I don't have to scroll through a long list to find the one I'm looking for.

- As an applicant with multiple applications, I want to be able to sort applications based on the date, status or name, so I can save the time.

- As a user concerned about privacy, I want to log in to my own private account, so that other people cannot see which companies I am applying to.


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

See instructions. Delete this line and place a link to the task boards here.
