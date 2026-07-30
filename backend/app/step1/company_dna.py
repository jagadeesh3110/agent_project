from openai import OpenAI
from app.config import settings
from app.step1.models import CompanyDNA, CompanyProfile


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


SYSTEM_PROMPT = """
You are an executive search intelligence analyst. Extract structured company
intelligence from the provided text. Focus on facts, avoid speculation.
""".strip()


def extract_company_dna(source_text: str, source_url: str | None = None) -> CompanyDNA:
    client = _get_client()
    response = client.beta.chat.completions.parse(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Extract company intelligence from the following source:\n\n"
                    f"{source_text}\n\n"
                    f"Return a structured CompanyProfile."
                ),
            },
        ],
        response_format=CompanyProfile,
    )
    profile = response.choices[0].message.parsed
    return CompanyDNA(
        profile=profile,
        intelligence_summary=_summarize(profile),
        data_completeness=_compute_completeness(profile),
    )


def _summarize(profile: CompanyProfile) -> str:
    parts = [f"{profile.name} is a {profile.industry} company."]
    if profile.description:
        parts.append(profile.description)
    if profile.mission:
        parts.append(f"Mission: {profile.mission}")
    if profile.strengths:
        parts.append(f"Key strengths: {'; '.join(profile.strengths[:3])}")
    return " ".join(parts)


def _compute_completeness(profile: CompanyProfile) -> float:
    fields = [
        profile.name != "",
        profile.industry != "",
        profile.headquarters is not None,
        profile.founded_year is not None,
        profile.employee_count is not None,
        profile.revenue is not None,
        profile.description is not None,
        profile.mission is not None,
        len(profile.values) > 0,
        len(profile.products_services) > 0,
        len(profile.competitors) > 0,
        len(profile.strengths) > 0,
    ]
    return sum(fields) / len(fields)
