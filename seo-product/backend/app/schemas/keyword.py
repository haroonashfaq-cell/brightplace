from pydantic import BaseModel
from datetime import datetime


class KeywordGapResponse(BaseModel):
    id: str
    project_id: str
    keyword: str
    volume: int
    kd: int
    intent: str | None
    competitor_domains: list[str]
    cpc: float | None = 0
    difficulty: str | None = None
    category: str | None = None
    city: str | None = None
    is_long_tail: bool | None = False
    tier: str | None = None
    word_count: int | None = 0
    fetched_at: datetime


class KeywordGapListResponse(BaseModel):
    items: list[KeywordGapResponse]
    total_count: int
    page: int
    page_size: int


class LongTailResponse(BaseModel):
    id: str
    keyword_gap_id: str
    keyword: str
    volume: int
    kd: int
    intent: str | None


class KeywordImportItem(BaseModel):
    keyword: str
    volume: int = 0
    kd: int = 0
    cpc: float = 0
    intent: str | None = None
    category: str | None = None
    city: str | None = None


class KeywordImportRequest(BaseModel):
    keywords: list[KeywordImportItem]
    replace: bool = False  # If true, replace all existing keywords


class SelectedKeywordCreate(BaseModel):
    keyword: str
    volume: int = 0
    kd: int = 0
    intent: str | None = None
    long_tail_keywords: list[dict] = []


class SelectedKeywordResponse(BaseModel):
    id: str
    project_id: str
    keyword: str
    volume: int
    kd: int
    intent: str | None
    long_tail_keywords: list[dict]
    status: str
    created_at: datetime
