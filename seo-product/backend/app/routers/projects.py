from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    CompetitorCreate,
    CompetitorResponse,
)
from app.services import project_service

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    body: ProjectCreate, user: dict = Depends(get_current_user)
):
    project = await project_service.create_project(
        user["id"], body.domain, body.niche
    )
    return project


@router.get("", response_model=list[ProjectResponse])
async def list_projects(user: dict = Depends(get_current_user)):
    return await project_service.get_projects(user["id"])


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, user: dict = Depends(get_current_user)):
    project = await project_service.get_project(project_id, user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str, user: dict = Depends(get_current_user)
):
    deleted = await project_service.delete_project(project_id, user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post(
    "/{project_id}/competitors/detect",
    response_model=list[CompetitorResponse],
)
async def detect_competitors(
    project_id: str, user: dict = Depends(get_current_user)
):
    competitors = await project_service.detect_competitors(
        project_id, user["id"]
    )
    return competitors


@router.post(
    "/{project_id}/competitors",
    response_model=CompetitorResponse,
    status_code=201,
)
async def add_competitor(
    project_id: str,
    body: CompetitorCreate,
    user: dict = Depends(get_current_user),
):
    comp = await project_service.add_competitor(
        project_id, user["id"], body.domain
    )
    if not comp:
        raise HTTPException(status_code=404, detail="Project not found")
    return comp


@router.get(
    "/{project_id}/competitors", response_model=list[CompetitorResponse]
)
async def list_competitors(
    project_id: str, user: dict = Depends(get_current_user)
):
    return await project_service.get_competitors(project_id, user["id"])


@router.delete("/{project_id}/competitors/{competitor_id}", status_code=204)
async def delete_competitor(
    project_id: str,
    competitor_id: str,
    user: dict = Depends(get_current_user),
):
    deleted = await project_service.delete_competitor(
        project_id, competitor_id, user["id"]
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
