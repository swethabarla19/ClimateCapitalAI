# Gemini on Vertex AI Configuration

ClimateCapital uses Gemini only for bounded explanation. The deterministic
application calculates Funding Priority and Funding Plans; Gemini cannot alter
project evidence, membership, boundary resolution, benchmark values, or governed
geometry.

## Runtime environment

Configure the FastAPI process with non-secret environment variables:

```text
GOOGLE_CLOUD_PROJECT=climatecapital-ai
GOOGLE_CLOUD_LOCATION=global
GEMINI_MODEL=gemini-3.5-flash
GEMINI_ENABLED=true
GEMINI_TIMEOUT_SECONDS=20
```

`GEMINI_ENABLED` defaults to `false`, so normal startup, bootstrap, Funding Plan,
Historical Benchmark, Explore, Help, methodology, and map behavior remain usable
without Google credentials or provider availability. The model and location are
read through one backend configuration boundary. React receives no Gemini key,
credential, token, or provider configuration.

## Local authentication

The official `google-genai` Python SDK uses Application Default Credentials in
Vertex AI mode. Establish developer ADC outside the application when needed:

```shell
gcloud auth application-default login
```

Application code does not manually load a service-account JSON key and does not
set `GOOGLE_APPLICATION_CREDENTIALS` to a repository file. Never commit a key or
ADC material.

## Cloud Run compatibility

Cloud Run should use a dedicated user-managed service account with the minimum
required Vertex permission, expected to be `roles/aiplatform.user`. Workload
identity/ADC supplies credentials automatically; no API Studio key or Secret
Manager entry is required for Gemini under this design.

## Governed provider boundary

- `POST /api/v1/gemini/explain` is the only public Gemini endpoint.
- The backend validates the active data/release identity and resolves all evidence.
- Funding Plan and boundary requests re-run the deterministic evaluator.
- Historical Benchmark grounding is retrospective and cannot enter selection.
- The provider receives a centralized January 21, 2026 system instruction and a
  bounded surface-specific grounding packet.
- Generation is non-streaming structured JSON with one candidate,
  `thinking_level=LOW`, and at most 1,200 output tokens.
- No Search, Maps, URL retrieval, web grounding, function calling, code execution,
  or other Gemini tool is configured.
- Runtime-v3 map context includes only governed role/provenance/caveat metadata;
  polygon coordinates are not sent. Unmapped projects remain explicitly location
  unavailable and are never geocoded or inferred.

Gemini is explanation-only and limited to the January 21, 2026 historical
snapshot. Provider failure is local to the drawer; authoritative deterministic
application state remains intact.
