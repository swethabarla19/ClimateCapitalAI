"""Machine-enforced identities already approved in repository authority.

These values encode the existing source registry, GCS preservation records, and
locked decisions. They do not register a new source or assert a new source fact.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class RegisteredSourceIdentity:
    publisher: str
    title: str
    source_url: str
    source_vintage: str
    published_date: str | None
    retrieval_timestamp: str | None
    sha256: str
    byte_size: int
    gcs_uri: str
    gcs_generation: str
    historical_fit: str
    analytical_role: str
    license_reuse_status: str


REGISTERED_SOURCE_IDENTITIES = MappingProxyType(
    {
        "austin_wpd_2026_bond_projects_2025_11_21": RegisteredSourceIdentity(
            publisher="City of Austin - Watershed Protection Department",
            title="Austin Watershed Protection Potential 2026 Bond Projects",
            source_url="https://services.austintexas.gov/edims/document.cfm?id=463345",
            source_vintage="2025-11-21 planning snapshot",
            published_date="2025-11-21",
            retrieval_timestamp="2026-08-31T19:57:53Z",
            sha256="d1c2731cc12ecb3938569d29ec0c92d0966d7706af919e0a519b48329493d88e",
            byte_size=1_151_348,
            gcs_uri="gs://climatecapital-ai-raw-swetha/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf",
            gcs_generation="1788210198102506",
            historical_fit="HISTORICALLY_VALID",
            analytical_role="analytical",
            license_reuse_status="UNVERIFIED",
        ),
        "austin_2026_bond_initial_draft_2026_01_21": RegisteredSourceIdentity(
            publisher="City of Austin - Capital Delivery Services",
            title="2026 Bond Initial Draft Project Recommendation",
            source_url="https://services.austintexas.gov/edims/document.cfm?id=466344",
            source_vintage="2026-01-21 initial draft recommendation",
            published_date="2026-01-21",
            retrieval_timestamp="2026-08-31T19:57:54Z",
            sha256="da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359",
            byte_size=412_820,
            gcs_uri="gs://climatecapital-ai-raw-swetha/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf",
            gcs_generation="1788210202820922",
            historical_fit="HISTORICALLY_VALID",
            analytical_role="benchmark",
            license_reuse_status="UNVERIFIED",
        ),
        "austin_rna_projects_layer_8_live": RegisteredSourceIdentity(
            publisher="City of Austin",
            title="Austin RNA Projects - RNA Projects Layer 8",
            source_url="https://maps.austintexas.gov/arcgis/rest/services/LongRangeCIP/RNAProjects/MapServer/8",
            source_vintage="Live/current service; content vintage unknown",
            published_date=None,
            retrieval_timestamp="2026-09-01T18:33:23Z",
            sha256="471dd527d9811ccd85cbfb9db71e6323b9ac28fa3746ad51bdcc97fbcb48bfd9",
            byte_size=32_774_832,
            gcs_uri="gs://climatecapital-ai-raw-swetha/raw/city_austin/rna_projects/layer_8/20260901T183323Z/features.arcgis.json",
            gcs_generation="1788287767379062",
            historical_fit="HISTORICAL_FIT_UNCERTAIN",
            analytical_role="research-only",
            license_reuse_status="UNVERIFIED",
        ),
    }
)
