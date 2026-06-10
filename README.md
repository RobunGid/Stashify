<p align="center">
  <h1 align="center">📚 Stashify</h1>
  <p align="center"><strong>Knowledge Resource Manager — Telegram bot for organizing, rating and discovering learning materials</strong></p>
  <p align="center"></p>
</p>

**Stashify** is a feature-rich Telegram bot for managing and sharing knowledge resources, built with an async-first architecture and a full role-based access system
 
- user registration with role and language assignment
- full CRUD for resources, categories and quizzes
- resource discovery via tag search and category browsing
- rating system and personal favorites
- quiz engine with questions and result tracking
- pagination for resource lists
- multilingual interface via Fluent
### Tech Stack
 
- **Aiogram** — async Telegram bot framework
- **SQLAlchemy** — async ORM with PostgreSQL backend
- **asyncpg** — high-performance async PostgreSQL driver
- **Pydantic & Pydantic Settings** — data validation and config management
- **aiogram-i18n + Fluent** — internationalization runtime
- **Alembic** — database migrations
- **PostgreSQL** — primary relational database
Built with scalability, clean schema design, and a smooth Telegram UX in mind
 
## How to Use
 
1. **Clone the repository and move into it:**
```bash
git clone https://github.com/RobunGid/Stashify.git
cd Stashify
```
 
2. **Copy and fill .env file:**
```bash
cp .env.example .env
vim .env
```
 
3. **Run `make all` to start all containers:**
```bash
make all
```
 
### Make Commands
 
#### All Services
* `make all` — up all services (app, database)
* `make all-down` — down all services
#### App
* `make app` — up application container
* `make app-down` — down application container
* `make app-logs` — follow the logs in app container
* `make app-shell` — run app container shell
#### Database
* `make db` — up PostgreSQL container
* `make db-down` — down PostgreSQL container
* `make db-logs` — follow the logs in database container
* `make db-shell` — run database container shell
* `make db-ui-logs` — follow the logs in database ui viewer container
---
 
* `poetry run pre-commit run --all-files` — run all pre-commit hooks (linters, formatters)
## Project Roadmap

- [x] Set up project structure with aiogram, sqlalchemy, docker, basic config
- [x] Initialize PostgreSQL models: 
	- [x] Users
	- [x] Resources
	- [x] Quizes
	- [x] Quizes questions
	- [x] Quiz results
	- [x] Ratings
	- [x] Categories
	- [x] Favorites
- [x] Initialize Pydantic schemas

- [x] User registration, role and language assignment 
- [x] Role system: admin, manager, user 

- [x] Main menu
- [x] Adding new resource
- [x] Deleting resource
- [x] Editing resource
- [x] Adding new category
- [x] Deleting category
- [x] Editing category
- [x] Adding new quiz
- [x] Deleting quiz
- [x] Editing quiz
- [x] View resource list pagination by categories
- [x] View resource details
- [x] Search resources by tags, verification by author
- [x] Rate resource
- [x] Add resource to favorite

- [x] Add quiz to resource: multiple-choice questions
- [ ] Complete quiz for a resource
- [ ] Store user quiz results

- [ ] Report a resource (spam, incorrect, etc)
- [ ] Admin view of reported resources and resolution

- [ ] View user progress: completed tests, liked resources
- [ ] View global stats: most liked, most completed

- [ ] Changing user role
- [ ] User blocking and unblocking 

- [ ] Manager-only access to edit / delete resources
- [ ] Admin-only access to assign roles and block users

- [ ] Logging: user actions, test completions, likes, reports

- [ ] Localization of bot messages and command responses
