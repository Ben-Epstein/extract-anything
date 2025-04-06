from prefect import Flow
from prefect.blocks.notifications import SlackWebhook
from prefect.server.schemas.core import FlowRun
from prefect.server.schemas.states import State
from prefect.settings import PREFECT_UI_URL


async def notify_slack(flow: Flow, flow_run: FlowRun, state: State):
    slack_webhook_block = await SlackWebhook.aload("prefect-flow-failures")
    # We need to type: ignore because of some prefect async issues
    # For more details: https://github.com/PrefectHQ/prefect/issues/15008
    await slack_webhook_block.notify(  # type: ignore
        (
            f"Your job {flow_run.name} entered {state.name} "
            f"with message:\n\n"
            f"See <{PREFECT_UI_URL.value()}/flow-runs/"
            f"flow-run/{flow_run.id}|the flow run in the UI>\n\n"
            f"Tags: {flow_run.tags}\n\n"
            f"Scheduled start: {flow_run.expected_start_time}"
        )
    )
