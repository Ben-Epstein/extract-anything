export VIRTUAL_ENV=.venv

.PHONY: baml-compile
baml-compile:
	uv run baml-cli generate --from ./baml_src

setup:
	uv venv && source .venv/bin/activate
	uv sync
	npm install -g pnpm
	npm install next react react-dom
	(cd frontend && npm install)
	HOMEBREW_NO_AUTO_UPDATE=1 brew install poppler
	make baml-compile

ui:
	(cd frontend && npm run dev)

server:
	uv run python src/shared/server.py

modal-auth:
	uv run modal setup
	uv run modal token new

prefect-auth:
	uv run prefect cloud login

modal-deploy-llama:
	uv run modal deploy -m modals.llama_modal.llama_3_2_11b --tag=`git rev-parse --short HEAD`

modal-deploy-all:
	make modal-deploy-llama

prefect-deploy: setup
	uv run prefect deploy --all --prefect-file ./src/flows/prefect.yaml

show-prefect-profile:
	uv run prefect profile inspect


.PHONY: format
format:
	uv --quiet run ruff format src
	uv --quiet run ruff check --fix src

.PHONY: lint
lint:
	uv --quiet run ruff check src
	uv --quiet run ruff format --check src
	uv --quiet run mypy src
