from pathlib import Path
import asyncio
import pathlib
from prefect import flow
import polars as pl
from typing import TypedDict
from prefect import task
from prefect.tasks import task_input_hash
from datetime import timedelta
from shared.baml_client.async_client import b
from shared.baml_client import types
from shared.pdf_processor import (
    convert_pdf_to_single_image,
    extract_milestones,
    extract_parties,
    extract_risks,
    flatten_nda,
)
from deltalake import DeltaTable


ROOT = pathlib.Path(__file__).parent.parent.parent
DELTA_OUT = ROOT / "processed"
DELTA_IN = ROOT / "raw"


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


@task(
    log_prints=True, cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1)
)
async def process_pdf(pdf_path: Path) -> ProcessedPDF:
    filename = pdf_path.name
    nda_data = await extract_nda_data(pdf_path)
    risk_analysis, deadline_report = await asyncio.gather(
        analyze_nda_risks(nda_data), track_nda_deadlines(nda_data)
    )
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


def write_delta(df: pl.DataFrame, table: Path | str) -> None:
    if DeltaTable.is_deltatable(str(table)):
        df.write_delta(
            table,
            mode="merge",
            delta_merge_options={
                "predicate": "s.nda_id = t.nda_id",
                "source_alias": "s",
                "target_alias": "t",
            },
        ).when_matched_update_all().when_not_matched_insert_all().execute()
    else:
        df.write_delta(table)


@flow(
    log_prints=True,
    # on_failure=[notify_slack],  # type: ignore
    # on_crashed=[notify_slack],  # type: ignore
    # on_cancellation=[notify_slack],  # type: ignore
    flow_run_name="process_ndas",
)
async def main(pdf_dir: str | Path):
    """Process all NDAs in a directory."""
    pdf_paths = [p for p in Path(pdf_dir).iterdir() if p.suffix == ".pdf"]
    tasks = [process_pdf(pdf_path) for pdf_path in pdf_paths]
    processed_pdfs = await asyncio.gather(*tasks)

    ndas_df = pl.concat([pdf["nda"] for pdf in processed_pdfs])
    parties_df = pl.concat([pdf["parties"] for pdf in processed_pdfs])
    risks_df = pl.concat([pdf["risks"] for pdf in processed_pdfs])
    milestones_df = pl.concat([pdf["milestones"] for pdf in processed_pdfs])

    dfs = [ndas_df, parties_df, risks_df, milestones_df]
    tables = ["ndas", "parties", "risks", "milestones"]
    for df, table in zip(dfs, tables):
        write_delta(fill_null(df), DELTA_OUT / table)


if __name__ == "__main__":
    asyncio.run(main(DELTA_IN))
