from pydantic import BaseModel
from datetime import datetime


# ============================================================
# Research
# ============================================================

class SerpItem(BaseModel):
    position: int = 0
    title: str = ""
    url: str = ""
    description: str = ""
    word_count: int | None = None

class SerpData(BaseModel):
    organic_results: list[SerpItem] = []
    featured_snippet: str | None = None
    ai_overview: str | None = None
    total_results: int = 0

class PaaItem(BaseModel):
    question: str
    competitor_answers: bool = False
    gap: bool = False

class PaaData(BaseModel):
    questions: list[PaaItem] = []

class RedditInsight(BaseModel):
    pain_points: list[str] = []
    real_numbers: list[str] = []
    misconceptions: list[str] = []
    advice: list[str] = []
    common_questions: list[str] = []

class ResearchReportResponse(BaseModel):
    id: str
    keyword_id: str
    project_id: str
    keyword: str
    serp_data: dict = {}
    paa_data: dict = {}
    reddit_data: dict = {}
    ai_mode_data: dict = {}
    status: str
    created_at: datetime
    updated_at: datetime


# ============================================================
# Brief
# ============================================================

class OutlineSection(BaseModel):
    heading: str
    level: int = 2  # H2 or H3
    instructions: str = ""
    subsections: list[dict] = []

class FaqItem(BaseModel):
    question: str
    answer: str

class CtaPlacement(BaseModel):
    position: str  # "after_first_h2", "mid_article", "end"
    text: str
    url: str = "https://app.brightplace.ai"

class BriefResponse(BaseModel):
    id: str
    research_report_id: str
    project_id: str
    keyword: str
    title: str | None
    seo_title: str | None
    meta_description: str | None
    slug: str | None
    outline: list = []
    target_keywords: dict = {}
    entities: list = []
    faqs: list = []
    ctas: list = []
    internal_links: list = []
    word_count_target: int = 2000
    snippet_paragraph: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class BriefUpdate(BaseModel):
    title: str | None = None
    seo_title: str | None = None
    meta_description: str | None = None
    slug: str | None = None
    outline: list | None = None
    target_keywords: dict | None = None
    entities: list | None = None
    faqs: list | None = None
    ctas: list | None = None
    internal_links: list | None = None
    word_count_target: int | None = None
    snippet_paragraph: str | None = None


# ============================================================
# Article
# ============================================================

class QaCheckResult(BaseModel):
    name: str
    passed: bool
    issues: list[str] = []
    suggestions: list[str] = []

class ArticleResponse(BaseModel):
    id: str
    brief_id: str
    project_id: str
    keyword: str
    title: str | None
    content_md: str | None
    content_html: str | None
    word_count: int = 0
    seo_score: int = 0
    qa_report: dict = {}
    status: str
    created_at: datetime
    updated_at: datetime


# ============================================================
# Pipeline Jobs
# ============================================================

class PipelineJobResponse(BaseModel):
    id: str
    project_id: str
    keyword_id: str
    step: str
    status: str
    result: dict = {}
    error: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class PipelineStatusResponse(BaseModel):
    keyword_id: str
    keyword: str
    steps: dict[str, PipelineJobResponse | None] = {}
    research_report: ResearchReportResponse | None = None
    brief: BriefResponse | None = None
    article: ArticleResponse | None = None
