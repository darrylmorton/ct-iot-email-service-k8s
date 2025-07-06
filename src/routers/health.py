from http import HTTPStatus

from fastapi import APIRouter
from starlette.responses import JSONResponse

from utils.app_util import AppUtil

router = APIRouter()


@router.get("/healthz")
async def health() -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "ok", "version": AppUtil.get_app_version()},
    )
