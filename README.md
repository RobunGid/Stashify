# Stashify

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
- [x] Initialize Pydantic schemas

- [ ] User registration, role and language assignment 
- [ ] Role system: admin, manager, user 

- [ ] View resource list with pagination
- [ ] View resource details
- [ ] Adding new resource
- [ ] Search resources by tags, verification by author
- [ ] Rate resource

- [ ] Add quiz to resource: multiple-choice questions
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
