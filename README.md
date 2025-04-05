# Extract Anything

Adapted from https://github.com/BoundaryML/baml-examples/tree/hellovai/extract-anything

Mainly with a modal deployment of llama-3.2-11b for extraction

# Full CI/CD workflows

This repo comes equipt to run prefect jobs on modal, processing raw documents with baml. To configure prefect and modal, follow [this guide](https://docs.prefect.io/v3/deploy/infrastructure-examples/modal). See the Makefile for some helpful aliases.

## Required repo secrets
* `MODAL_TOKEN_ID`: https://modal.com/settings/[YOUR_ACCOUNT]/member-tokens
* `MODAL_TOKEN_SECRET`: https://modal.com/settings/[YOUR_ACCOUNT]/member-tokens
* `SLACK_BOT_TOKEN`: https://api.slack.com/tutorials/tracks/getting-a-token 
* `PREFECT_API_KEY`: See the output of `make show-prefect-profile` (after running `make prefect-auth`)
* `PREFECT_API_URL`: See the output of `make show-prefect-profile` (after running `make prefect-auth`)

## Requred .env values
This depends on what LLM you're using. If OpenAI, then the standard OPENAI_API_KEY, if vertex, then the path to your vertex-json credentials. See the `.env.copy` for examples.