from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_current_user
from app.schemas.keyword import (
    KeywordGapListResponse,
    KeywordImportRequest,
    LongTailResponse,
    SelectedKeywordCreate,
    SelectedKeywordResponse,
)
from app.services import keyword_service

router = APIRouter(prefix="/api/projects/{project_id}", tags=["keywords"])


@router.get("/keyword-gaps", response_model=KeywordGapListResponse)
async def list_keyword_gaps(
    project_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    kd_min: int | None = Query(None),
    kd_max: int | None = Query(None),
    vol_min: int | None = Query(None),
    vol_max: int | None = Query(None),
    intent: str | None = Query(None),
    search: str | None = Query(None),
    category: str | None = Query(None),
    sort_by: str = Query("volume"),
    sort_dir: str = Query("desc"),
    user: dict = Depends(get_current_user),
):
    return await keyword_service.get_keyword_gaps(
        project_id=project_id,
        user_id=user["id"],
        page=page,
        page_size=page_size,
        kd_min=kd_min,
        kd_max=kd_max,
        vol_min=vol_min,
        vol_max=vol_max,
        intent=intent,
        search=search,
        category=category,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )


@router.get("/keyword-gaps/categories")
async def list_categories(
    project_id: str, user: dict = Depends(get_current_user)
):
    return await keyword_service.get_categories(project_id, user["id"])


@router.post("/keyword-gaps/refresh")
async def refresh_keyword_gaps(
    project_id: str, user: dict = Depends(get_current_user)
):
    return await keyword_service.refresh_keyword_gaps(project_id, user["id"])


@router.post("/keyword-gaps/import")
async def import_keywords(
    project_id: str,
    body: KeywordImportRequest,
    user: dict = Depends(get_current_user),
):
    return await keyword_service.import_keywords(
        project_id, user["id"], body.keywords, body.replace
    )


@router.get(
    "/keyword-gaps/{gap_id}/long-tail",
    response_model=list[LongTailResponse],
)
async def get_long_tail(
    project_id: str,
    gap_id: str,
    user: dict = Depends(get_current_user),
):
    return await keyword_service.get_long_tail(project_id, gap_id, user["id"])


@router.post(
    "/selected-keywords",
    response_model=SelectedKeywordResponse,
    status_code=201,
)
async def add_selected_keyword(
    project_id: str,
    body: SelectedKeywordCreate,
    user: dict = Depends(get_current_user),
):
    result = await keyword_service.add_selected_keyword(
        project_id=project_id,
        user_id=user["id"],
        keyword=body.keyword,
        volume=body.volume,
        kd=body.kd,
        intent=body.intent,
        long_tail_keywords=body.long_tail_keywords,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@router.get("/selected-keywords", response_model=list[SelectedKeywordResponse])
async def list_selected_keywords(
    project_id: str, user: dict = Depends(get_current_user)
):
    return await keyword_service.get_selected_keywords(project_id, user["id"])


@router.delete("/selected-keywords/{keyword_id}", status_code=204)
async def delete_selected_keyword(
    project_id: str,
    keyword_id: str,
    user: dict = Depends(get_current_user),
):
    deleted = await keyword_service.delete_selected_keyword(
        project_id, keyword_id, user["id"]
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
