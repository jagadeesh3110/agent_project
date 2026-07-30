from openai import OpenAI
from app.config import settings
from app.step1.models import RoleIntelligence, RoleRequirement, ReportingStructure


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


SYSTEM_PROMPT = """
You are an executive search intelligence analyst. Extract structured role
intelligence from the provided text. Focus on factual role requirements,
responsibilities, and qualifications. Avoid speculation.
""".strip()


def extract_role_intelligence(
    source_text: str,
    source_url: str | None = None,
) -> RoleIntelligence:
    client = _get_client()
    response = client.beta.chat.completions.parse(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Extract role intelligence from the following source:\n\n"
                    f"{source_text}\n\n"
                    f"Return a structured RoleIntelligence."
                ),
            },
        ],
        response_format=RoleIntelligence,
    )
    parsed = response.choices[0].message.parsed
    parsed.intelligence_summary = _summarize(parsed)
    parsed.data_completeness = _compute_completeness(parsed)
    return parsed


def _summarize(role: RoleIntelligence) -> str:
    parts = [f"Role: {role.title}"]
    if role.department:
        parts.append(f"Department: {role.department}")
    if role.key_skills:
        parts.append(f"Key skills: {'; '.join(role.key_skills[:5])}")
    if role.responsibilities:
        parts.append(f"Top responsibility: {role.responsibilities[0]}")
    return " | ".join(parts)


def _compute_completeness(role: RoleIntelligence) -> float:
    fields = [
        role.title != "",
        role.department is not None,
        len(role.responsibilities) > 0,
        len(role.requirements) > 0,
        len(role.key_skills) > 0,
        role.experience_years is not None,
        role.education is not None,
        len(role.personality_traits) > 0,
        len(role.challenges) > 0,
        len(role.kpis) > 0,
    ]
    return sum(fields) / len(fields)
