import datetime
import os
from dateutil.parser import parse
import asyncio
from pdf2image import convert_from_bytes
from shared.baml_client import b, types
from baml_py import Image
from PIL import Image as PILImage
import io
from base64 import b64encode as b64e
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent
PDF_RAW = HERE.parent.parent / "raw"


def convert_pdf_to_single_image(pdf_bytes):
    """Convert PDF bytes to a single combined image.

    We do this because, while OpenAI and other closed models can handle many images, Llama-3.2-14b-vision cannot.
    So we give it a single image of all pdf pages combined.
    """

    page_images = convert_from_bytes(pdf_bytes)
    width = max(img.width for img in page_images)
    total_height = sum(img.height for img in page_images)

    # Create a new blank image with the calculated dimensions
    combined_image = PILImage.new("RGB", (width, total_height), color="white")

    # Paste each page into the combined image
    y_offset = 0
    for img in page_images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    buffered = io.BytesIO()
    combined_image.save(buffered, format="JPEG")
    return Image.from_base64(
        base64=b64e(buffered.getvalue()).decode("utf-8"), media_type="image/jpeg"
    )


def flatten_nda(
    nda_data: types.NDA, deadlines: types.DeadlineReport, filename: str
) -> dict[str, Any]:
    """Flatten NDA object for DataFrame conversion."""
    return {
        "nda_id": os.path.splitext(filename)[0],
        "title": nda_data.title,
        "effective_date": nda_data.effective_date,
        "agreement_type": nda_data.agreement_type.name,
        "term_duration_length": nda_data.term_duration.length,
        "term_duration_unit": nda_data.term_duration.unit.name,
        "confidentiality_period_length": nda_data.confidentiality_period.length,
        "confidentiality_period_unit": nda_data.confidentiality_period.unit.name,
        "governing_law": nda_data.governing_law,
        "conf_info_definition": nda_data.confidential_information.general_definition,
        "expiration_date": parse(deadlines.expiration_date.value),
        "confidentiality_end_date": parse(deadlines.confidentiality_end_date.value),
    }


def extract_parties(nda_data: types.NDA, filename: str) -> list[dict[str, Any]]:
    """Extract parties from NDA for DataFrame conversion."""
    parties = []
    for part_id, party in enumerate(nda_data.parties):
        parties.append(
            {
                "nda_id": os.path.splitext(filename)[0],
                "part": part_id,
                "party_name": party.name,
                "party_type": party.type,
                "party_role": party.role.name,
                "street": party.address.street,
                "city": party.address.city,
                "state": party.address.state,
                "zip": party.address.zip,
                "country": party.address.country,
                "contact_name": party.contact_person.name
                if party.contact_person
                else None,
                "contact_title": party.contact_person.title
                if party.contact_person
                else None,
                "contact_email": party.contact_person.email
                if party.contact_person
                else None,
            }
        )
    return parties


def extract_risks(
    risk_analysis: types.RiskAnalysis, filename: str
) -> list[dict[str, Any]]:
    """Extract risks from risk analysis for DataFrame conversion."""
    risks = []
    for part_id, risk in enumerate(risk_analysis.key_risks):
        risks.append(
            {
                "nda_id": os.path.splitext(filename)[0],
                "part": part_id,
                "section": risk.section,
                "description": risk.description,
                "severity": risk.severity.name,
                "potential_impact": risk.potential_impact,
                "overall_risk_level": risk_analysis.overall_risk_level.value,
            }
        )
    return risks


def extract_milestones(
    deadlines: types.DeadlineReport, filename: str
) -> list[dict[str, int | str | datetime.date]]:
    return [
        {
            "nda_id": os.path.splitext(filename)[0],
            "part": part_id,
            "name": milestones.name,
            "date": parse(milestones.date.value),
            "description": milestones.description,
        }
        for part_id, milestones in enumerate(deadlines.key_milestones)
    ]


# def convert_to_baml_image(img: PpmImageFile) -> Image:
#     buffered = io.BytesIO()
#     img.save(buffered, format="JPEG")
#     return Image.from_base64(base64=b64e(buffered.getvalue()).decode("utf-8"), media_type="image/jpeg")


async def process_nda_pdf(pdf_path: str | Path) -> dict:
    """Process an NDA PDF file through the BAML pipeline."""

    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()

    baml_image = convert_pdf_to_single_image(pdf_bytes)
    nda_data = await b.ExtractNDA(baml_image)
    risk_analysis, deadlines = await asyncio.gather(
        b.AnalyzeNDARisks(nda_data), b.TrackDeadlines(nda_data)
    )
    # If you wanted to pass many images
    # images: list[PpmImageFile] = convert_from_bytes(pdf_bytes) # type: ignore
    # baml_images = [convert_to_baml_image(image) for image in images]
    # nda_data = await b.ExtractNDA(baml_images)

    return {"nda": nda_data, "risks": risk_analysis, "deadlines": deadlines}


if __name__ == "__main__":
    res = asyncio.run(process_nda_pdf(PDF_RAW / "NDA1.pdf"))
    print(res)
