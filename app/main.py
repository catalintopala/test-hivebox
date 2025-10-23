"""
Main module which defines the root endpoint.
"""

from fastapi import FastAPI

from .routers import temperature, version

app = FastAPI()

app.include_router(version.router)
app.include_router(temperature.router)


@app.get("/")
async def root():
    """
    Handle GET requests to the root endpoint.
    """
    return {"message": "Hello World"}
