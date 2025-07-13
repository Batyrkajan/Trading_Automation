🚀 Project Awareness & Context

Read PLANNING.md before coding.

Check TASK.md before starting a new task; add missing tasks with a brief description and today's date.

Follow consistent naming conventions (snake_case, PascalCase) and project architecture.

Use .env for secrets management.

🧱 Code Structure & Modularity

Keep files under 300–500 lines; split when approaching this limit.

Organize by feature and responsibility:

app/ → Trading system modules.

tests/ → Tests for each module.

Prefer relative imports for clarity.

Use docstrings and inline comments for non-obvious logic.

🧪 Testing & Reliability

Write unit tests for all significant logic.

Cover at least:

Normal cases

Edge cases

Failure scenarios

Use pytest for consistency.

✅ Task Management

Mark completed tasks in TASK.md.

Add new subtasks discovered during development under "Discovered During Work."

🎨 Style & Conventions

Follow consistent formatting with black and flake8.

Use type hints throughout (-> str, -> None).

Keep environment configurations flexible and secure.

📚 Documentation

Keep README.md updated with clear setup and usage instructions.

Comment complex or critical design decisions inline.

🌐 Git & Deployment

Use clear, descriptive commit messages.

Commit after meaningful units of work (features, tests, fixes).

Use feature branches (feature/xyz) for isolation.

Add deployment instructions in DEPLOYMENT.md if Dockerized.

🤖 AI Code Agent Behavior Rules

Never hallucinate code or dependencies.

Verify file paths and structures before referencing.

Do not overwrite existing code unless explicitly instructed or part of a documented task.

Ask clarifying questions if context is missing.

🪄 Optional Advanced Practices

Add architecture diagrams if the system expands.

Use semantic versioning tags for releases.

Add a docs/ folder for future advanced documentation.