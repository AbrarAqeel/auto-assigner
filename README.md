# Auto Assigner

A Flask + MySQL web application that automatically distributes incoming customer service forms (tickets) to available agents using a priority-weighted, round-robin assignment algorithm. The system includes three separate dashboards: one for customers submitting requests, one for supervisors managing agents, and one for agents handling assigned work.

## Features

- **Customer Dashboard** — submit a form/request with a type and description
- **Supervisor Dashboard** — add, update, and remove agents; adjust agent priority and workload capacity
- **Agent Dashboard** — agent login, view assigned form details, update status (Available / Working / Offline / Break), and mark forms as completed
- **Automatic Assignment Engine** — assigns unassigned forms to available agents in priority order using a round-robin approach that respects each agent's workload limit
- REST-style JSON endpoints for form status, agent status, and assignment triggering
- Soft-delete for agents via a `Visibility` flag rather than removing records outright

## Tech Stack

- Python, [Flask](https://flask.palletsprojects.com/)
- MySQL (via `mysql-connector-python`)
- HTML, CSS, JavaScript (Jinja templates + static assets)

## Project Structure

```
auto-assigner/
├── api.py            # Flask application: routes, DB access, assignment logic
├── SQLQuery.sql       # Database schema, triggers, and seed data
├── static/            # CSS/JS assets
├── templates/          # Jinja2 HTML templates (dashboards, login, etc.)
└── README.md
```

## Database Schema

The app uses a MySQL database named `Meezanship` with three core tables:

- **Agents** — `Agent_ID`, `Agent_Name`, `Agent_Priority` (0.01–0.99), `Agent_Workload`, `Agent_Status` (`Available`/`Working`/`Offline`/`Break`), `Visibility`
- **Agents_Login** — login credentials linked to an `Agent_ID`
- **Forms** — submitted customer requests, with `Form_Status` (`Unassigned`/`Assigned`/`Completed`) and a foreign key to the assigned agent

Two triggers validate that `Agent_Name` and `Form_Type` do not contain special characters.

## Prerequisites

- Python 3.9+
- MySQL Server
- `pip` packages: `flask`, `mysql-connector-python`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AbrarAqeel/auto-assigner.git
   cd auto-assigner
   ```

2. Install dependencies:
   ```bash
   pip install flask mysql-connector-python
   ```

3. **Make sure `SQLQuery.sql`, the `static/` folder, and the `templates/` folder are all present in the project directory** — the app depends on them to run correctly.

4. Set up the database. Run the contents of `SQLQuery.sql` in your MySQL client to create the `Meezanship` database, its tables, triggers, and seed data:
   ```bash
   mysql -u root -p < SQLQuery.sql
   ```

5. Configure your database credentials (see **Security Notes** below before using this in anything beyond local development).

6. Run the app:
   ```bash
   python api.py
   ```

7. Visit `http://localhost:5000` in your browser.

## Usage

- **Customers** submit a form describing their request type and details from the customer dashboard.
- **Supervisors** add agents with a priority score and workload capacity, and can adjust these at any time.
- Trigger `/assign_forms` (POST) to run the assignment engine, which distributes all currently unassigned forms to available agents in priority order, respecting each agent's workload cap.
- **Agents** log in, view their currently assigned form, and mark it complete when finished.

## API Endpoints (Summary)

| Endpoint | Method | Description |
|---|---|---|
| `/submit-form` | POST | Customer submits a new form |
| `/supervisor-dashboard` | GET/POST | View/add agents |
| `/update_agent_priority` | POST | Update an agent's priority |
| `/update_agent_workload` | POST | Update an agent's workload capacity |
| `/delete_agent` | POST | Soft-delete an agent |
| `/assign_forms` | POST | Run the auto-assignment engine |
| `/agents_status` | GET | List all agents and their status |
| `/form_status` | GET | List all forms and their status |
| `/agent_login` | POST | Agent authentication |
| `/update_status` | POST | Update an agent's availability status |
| `/complete_form` | POST | Mark an agent's active form as completed |

## Security Notes

This project was built for demonstration/learning purposes and has several issues that **must** be addressed before any real-world or public deployment:

- **Hardcoded database credentials** are present directly in `api.py` and `SQLQuery.sql` (including a root password). Move these to environment variables or a `.env` file excluded from version control, e.g.:
  ```python
  import os
  host = os.environ["DB_HOST"]
  user = os.environ["DB_USER"]
  pwd = os.environ["DB_PASSWORD"]
  database = os.environ["DB_NAME"]
  ```
- **Plaintext passwords**: agent login passwords are stored and compared as plaintext (`password123` in the seed data). Use a hashing library such as `werkzeug.security` or `bcrypt` for real credential storage.
- **SQL structure is mostly parameterized**, which is good — continue using parameterized queries (`%s` placeholders) rather than string formatting when adding new routes.
- **Flask debug mode** (`app.run(debug=True)`) should be disabled in any production or publicly accessible deployment.
- Because the seed SQL grants root access with a hardcoded password, **rotate any credentials** if this schema has ever been deployed against a real database.

## Known Limitations

- There are two `/` routes defined (`index()` and `agent_dashboard()`), which will conflict — Flask will only register the first.
- The assignment algorithm currently checks workload by counting all forms ever assigned to an agent rather than only currently active ones, which may need revisiting depending on intended behavior.
- No environment-based configuration; all settings are currently hardcoded.

## License

No license specified. Add a `LICENSE` file if you'd like to define usage terms for others.
