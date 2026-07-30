from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CompanyProfile(BaseModel):
    name: str
    industry: str
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    revenue: Optional[str] = None
    description: Optional[str] = None
    mission: Optional[str] = None
    values: list[str] = []
    culture: Optional[str] = None
    products_services: list[str] = []
    competitors: list[str] = []
    strengths: list[str] = []
    weaknesses: list[str] = []
    recent_news: list[str] = []
    source_urls: list[str] = []


class CompanyDNA(BaseModel):
    profile: CompanyProfile
    intelligence_summary: Optional[str] = None
    extracted_at: date = Field(default_factory=date.today)
    data_completeness: float = Field(default=0.0, ge=0.0, le=1.0)


class RoleRequirement(BaseModel):
    category: str
    items: list[str] = []
    is_required: bool = True


class ReportingStructure(BaseModel):
    reports_to: Optional[str] = None
    direct_reports_count: Optional[int] = None
    team_size: Optional[int] = None
    department: Optional[str] = None


class RoleIntelligence(BaseModel):
    title: str
    department: Optional[str] = None
    reporting: ReportingStructure = Field(default_factory=ReportingStructure)
    responsibilities: list[str] = []
    requirements: list[RoleRequirement] = []
    preferred_qualifications: list[str] = []
    experience_years: Optional[int] = None
    education: Optional[str] = None
    key_skills: list[str] = []
    personality_traits: list[str] = []
    challenges: list[str] = []
    kpis: list[str] = []
    compensation_range: Optional[str] = None
    location: Optional[str] = None
    is_remote_ok: bool = False
    source_urls: list[str] = []
    intelligence_summary: Optional[str] = None
    extracted_at: date = Field(default_factory=date.today)
    data_completeness: float = Field(default=0.0, ge=0.0, le=1.0)
