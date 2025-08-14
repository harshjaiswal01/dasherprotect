up:
\tdocker compose up --build -d
down:
\tdocker compose down -v
logs:
\tdocker compose logs -f backend
test:
\tdocker compose exec -T backend pytest -q
fmt:
\techo "Add ruff/black later"
lint:
\techo "Add ruff/black later"
