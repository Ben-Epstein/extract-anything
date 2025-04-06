import asyncio
from typing import TypedDict

import polars as pl
from cloudpathlib import GSPath
from deltalake import DeltaTable
from prefect import flow, task
from prefect.tasks import task_input_hash

from flows.hooks import notify_slack
from shared.baml_client import types
from shared.baml_client.async_client import b
from shared.pdf_processor import (
    convert_pdf_to_single_image,
    extract_milestones,
    extract_parties,
    extract_risks,
    flatten_nda,
)

BUCKET = "gs://northeastern-pdf-ndas"
DELTA_OUT = "db"
DELTA_IN = "unprocessed"
PROCESSED_PDFS = "processed"


@task(retries=3, cache_key_fn=task_input_hash)
async def extract_nda_data(pdf_path) -> types.NDA:
    """Extract NDA data from a PDF file."""
    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()

    image = convert_pdf_to_single_image(pdf_bytes)
    return await b.ExtractNDA(image)


@task(retries=3, cache_key_fn=task_input_hash)
async def analyze_nda_risks(nda_data) -> types.RiskAnalysis:
    """Analyze risks in the NDA."""
    return await b.AnalyzeNDARisks(nda_data)


@task(retries=3, cache_key_fn=task_input_hash)
async def track_nda_deadlines(nda_data) -> types.DeadlineReport:
    """Track important deadlines in the NDA."""
    return await b.TrackDeadlines(nda_data)


class ProcessedPDF(TypedDict):
    nda: pl.DataFrame
    parties: pl.DataFrame
    risks: pl.DataFrame
    milestones: pl.DataFrame


@task(log_prints=True)
async def process_pdf(pdf_path: GSPath | str) -> ProcessedPDF:
    filename = GSPath(pdf_path).name
    nda_data = await extract_nda_data(pdf_path)
    risk_analysis, deadline_report = await asyncio.gather(analyze_nda_risks(nda_data), track_nda_deadlines(nda_data))
    return ProcessedPDF(
        nda=pl.from_dict(flatten_nda(nda_data, deadline_report, filename)),
        parties=pl.from_dicts(extract_parties(nda_data, filename)),
        risks=pl.from_dicts(extract_risks(risk_analysis, filename)),
        milestones=pl.from_dicts(extract_milestones(deadline_report, filename)),
    )


def fill_null(df: pl.DataFrame) -> pl.DataFrame:
    for col, dtype in zip(df.columns, df.dtypes):
        if isinstance(None, dtype.to_python()):  # TODO: Must be a better way
            df = df.with_columns(pl.col(col).cast(str).fill_null("N/A"))
    return df


def write_delta(df: pl.DataFrame, table: GSPath | str, part_id: bool) -> None:
    if DeltaTable.is_deltatable(str(table)):
        predicate = "s.nda_id = t.nda_id"
        if part_id:
            predicate += " AND s.part = t.part"
        df.write_delta(
            str(table),
            mode="merge",
            delta_merge_options={
                "predicate": predicate,
                "source_alias": "s",
                "target_alias": "t",
            },
        ).when_matched_update_all().when_not_matched_insert_all().execute()
    else:
        df.write_delta(str(table))


@flow(
    log_prints=True,
    on_failure=[notify_slack],  # type: ignore
    on_crashed=[notify_slack],  # type: ignore
    on_cancellation=[notify_slack],  # type: ignore
    flow_run_name="process_ndas",
)
async def main(pdf_dir: str | GSPath | None = None):
    """Process all NDAs in a directory."""
    pdf_dir = pdf_dir or GSPath(BUCKET) / DELTA_IN
    delta_out = GSPath(BUCKET) / DELTA_OUT
    pdf_paths = [p for p in GSPath(pdf_dir).iterdir() if p.name.endswith(".pdf")]
    tasks = [process_pdf(pdf_path) for pdf_path in pdf_paths]
    processed_pdfs = await asyncio.gather(*tasks)

    ndas_df = pl.concat([pdf["nda"] for pdf in processed_pdfs])
    parties_df = pl.concat([pdf["parties"] for pdf in processed_pdfs])
    risks_df = pl.concat([pdf["risks"] for pdf in processed_pdfs])
    milestones_df = pl.concat([pdf["milestones"] for pdf in processed_pdfs])

    dfs = [ndas_df, parties_df, risks_df, milestones_df]
    tables = ["ndas", "parties", "risks", "milestones"]
    for df, table in zip(dfs, tables):
        write_delta(fill_null(df), delta_out / table, part_id=True if table != "ndas" else False)


if __name__ == "__main__":
    asyncio.run(main())
