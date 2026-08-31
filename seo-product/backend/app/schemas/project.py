from pydantic import BaseModel
from datetime import datetime


class ProjectCreate(BaseModel):
    domain: str
    niche: str | None = None


class ProjectResponse(BaseModel):
    id: str
    user_id: str
    domain: str
    niche: str | None
    brand_context: dict
    created_at: datetime
    updated_at: datetime


class CompetitorCreate(BaseModel):
    domain: str


class CompetitorResponse(BaseModel):
    id: str
    project_id: str
    domain: str
    dr_score: int | None
    indexed_pages: int | None
    auto_detected: bool
    created_at: datetime
