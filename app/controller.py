"""FastAPI controllers for LLM registry CRUD."""

from fastapi import APIRouter, HTTPException, Request, status

from app.model_registry import ModelRegistry
from app.models import RegisteredLLM


router = APIRouter(prefix="/api/models", tags=["models"])


def _registry(request: Request) -> ModelRegistry:
    return request.app.state.model_registry


@router.get("", response_model=list[RegisteredLLM])
def list_models(request: Request) -> list[RegisteredLLM]:
    return _registry(request).list_models()


@router.post("", response_model=RegisteredLLM, status_code=status.HTTP_201_CREATED)
def create_model(model: RegisteredLLM, request: Request) -> RegisteredLLM:
    try:
        return _registry(request).create_model(model)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put("/{model_id}", response_model=RegisteredLLM)
def update_model(
    model_id: str,
    model: RegisteredLLM,
    request: Request,
) -> RegisteredLLM:
    if model.model_id != model_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path and body model IDs must match.",
        )

    updated = _registry(request).update_model(model_id, model)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found.",
        )
    return updated


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(model_id: str, request: Request) -> None:
    if not _registry(request).delete_model(model_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found.",
        )
