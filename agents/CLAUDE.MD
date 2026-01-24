# Inventory Management System

A Django REST Framework-based inventory management system for tracking products, departments, and purchase/sale orders.

## Project Overview

This is a backend API for managing inventory operations including:
- Product catalog management with automated pricing
- Department organization with margin calculations
- Purchase and sale order tracking
- User authentication with role-based permissions

## Tech Stack

- **Framework**: Django 4.2.3 with Django REST Framework 3.14.0
- **Database**: PostgreSQL (psycopg2 2.9.6)
- **Task Queue**: Celery 5.2.7 with Redis backend
- **Testing**: pytest 7.4.0, pytest-django 4.5.2, pytest-bdd 7.0.0
- **Containerization**: Docker with docker-compose

## Project Structure

```
inventory/
├── django_apps/
│   ├── authentication/    # User authentication & profiles
│   ├── products/         # Product & department management
│   └── orders/          # Purchase & sale orders
├── inventory/           # Django project settings
├── utils/              # Shared utilities & base models
├── fixtures/           # Test data fixtures
├── agents/             # AI agent documentation
├── Makefile           # Docker & Django commands
└── docker-compose.yml # Container orchestration
```

## Key Models

### Products App

**Departments** (`django_apps/products/models.py:7`)
- Fields: name, description, code, margin_percentage
- Defines profit margins for automatic pricing
- Uses BaseModel (auto-incrementing ID)

**Products** (`django_apps/products/models.py:34`)
- Fields: department, name, description, code, cost, price, stock
- Auto-calculates price based on cost and department margin
- Uses BaseModelUUID (UUID primary key)
- Price recalculated on save if cost changes

### Orders App

**PurchaseOrder** (`django_apps/orders/models.py:9`)
- Tracks incoming inventory
- Status: RECEIVED, CANCELLED
- Fields: product, quantity, unit_cost, total_cost, purchase_date

**SaleOrder** (`django_apps/orders/models.py:39`)
- Tracks outgoing sales
- Status: ACCEPTED, CANCELLED
- Fields: product, quantity, unit_price, total_price, sale_date

### Authentication App

**Profile** (`django_apps/authentication/models.py:7`)
- Extends Django User model
- Roles: admin, sale, purchase
- One-to-one relationship with User

## Architecture Patterns

The project follows a service/selector pattern:
- **Services** (`services.py`): Write operations and business logic
- **Selectors** (`selectors.py`): Read operations and queries
- **Views** (`views.py`): API endpoints using DRF
- **Tests**: BDD-style tests using pytest-bdd in `test/e2e/`

## Development Setup

### Using Docker (Recommended)

```bash
# Build containers
make build

# Start services
make up

# Run migrations
make migrate

# Create superuser
make create-superuser

# Load fixtures
make load-fixtures ARGS=/app/fixtures/departments.json
make load-fixtures ARGS=/app/fixtures/products.json
```

### Environment Variables

Set via `.envrc` or environment:
- `POSTGRES_DB`: Database name (default: inventory)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_HOST`: Database host (default: db)

## Testing

```bash
# Run all tests
make test

# Run with verbose output
make test ARGS="-v"

# Run specific test
make test ARGS="django_apps/products/test/e2e/products/views/step_defs/test_create_product.py"
```

Test organization:
- E2E tests use pytest-bdd with Gherkin scenarios
- Located in `django_apps/{app}/test/e2e/`
- Fixtures defined in `conftest.py`

## API Authentication

Uses Token Authentication:
- Basic Authentication
- Token Authentication (DRF tokens)

Configure in `inventory/settings.py:77`

## Common Tasks

### Database Operations

```bash
# Make migrations
make makemigrations

# Apply migrations
make migrate

# Reset database
make reset-db

# Dump data
make dump-data output=file.json model=app.Model
```

### Container Management

```bash
# Start in background
make up-d

# Stop containers
make stop

# Remove containers
make down

# View logs
docker compose logs -f web
```

### Django Shell

```bash
make shell
```

### Execute in Container

```bash
make docker-exec CONTAINER_ID=<id> ARGS=bash
```

## Important Implementation Notes

### Product Pricing Logic

Products automatically calculate price based on department margin:
```python
price = cost * (1 + department.margin_percentage/100)
```

This recalculates when:
- Product is created
- Product cost is updated

See `django_apps/products/models.py:79`

### Base Models

Two base models in `utils/models.py`:
- `BaseModel`: Auto-incrementing ID, created_at, updated_at
- `BaseModelUUID`: UUID primary key, created_at, updated_at

### Celery Tasks

Async tasks configured with Redis broker.
- Tasks defined in `django_apps/products/tasks.py`
- Configuration in `inventory/celery.py`

## File Locations

- Settings: `inventory/settings.py`
- URL routing: `inventory/urls.py`
- Main project: `inventory/`
- Apps: `django_apps/{authentication,products,orders}/`
- Shared utilities: `utils/`
- Test fixtures: `fixtures/`
- Agent docs: `agents/`

## Testing Strategy

The project uses BDD testing with pytest-bdd:
- Feature scenarios describe user stories
- Step definitions implement test logic
- Tests located in `test/e2e/` directories

Example test paths:
- Department tests: `django_apps/products/test/e2e/departments/views/step_defs/`
- Product tests: `django_apps/products/test/e2e/products/views/step_defs/`

## Common Issues

1. **Database connection**: Ensure PostgreSQL container is running
2. **Migrations**: Run `make migrate` after pulling changes
3. **Fixtures**: Load in correct order (departments before products)
4. **Celery**: Requires Redis container for task queue

## Git Workflow

Main branch: `main`
Current branch: `brave-leavitt`

Recent work includes:
- Docker configuration updates
- Product creation testing
- Department margin updates
- Orders migrations
