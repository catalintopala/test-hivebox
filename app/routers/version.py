"""
Version endpoint module.
"""

from fastapi import APIRouter

from .. import __version__

router = APIRouter()


@router.get("/version")
async def version():
    """
    Returns the version of the hivebox app.
    """
    return {"version": f"v{__version__}"}
