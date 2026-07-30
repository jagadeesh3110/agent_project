import asyncio
from dataclasses import dataclass
from app.config import settings
from app.step1.models import CompanyDNA, RoleIntelligence
from app.step1.company_dna import extract_company_dna
from app.step1.role_intelligence import extract_role_intelligence


@dataclass
class Step1Result:
    company_dna: CompanyDNA
    role_intelligence: RoleIntelligence | None
    sources_consumed: int


class Step1Orchestrator:

    def __init__(self) -> None:
        self._semaphore = asyncio.Semaphore(settings.STEP1_MAX_CONCURRENCY)

    async def run(
        self,
        company_sources: list[str],
        role_sources: list[str] | None = None,
    ) -> Step1Result:
        async with self._semaphore:
            dna = await asyncio.to_thread(
                extract_company_dna,
                self._join_sources(company_sources),
            )

        role_intel = None
        if role_sources:
            async with self._semaphore:
                role_intel = await asyncio.to_thread(
                    extract_role_intelligence,
                    self._join_sources(role_sources),
                )

        consumed = len(company_sources) + (len(role_sources) if role_sources else 0)
        return Step1Result(
            company_dna=dna,
            role_intelligence=role_intel,
            sources_consumed=consumed,
        )

    @staticmethod
    def _join_sources(sources: list[str]) -> str:
        return "\n\n---\n\n".join(sources)
