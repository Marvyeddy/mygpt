from fastapi import FastAPI
import sys
import asyncio

version = "v1"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title="MyGPT",
    description=(
        "MiGPT is an AI-powered conversational platform that offers:\n"
        "- Intelligent conversations\n"
        "- Persistent chat history\n"
        "- Document-based question answering using Retrieval-Augmented Generation (RAG)\n\n"
        "Technologies: FastAPI, PostgreSQL, and ChromaDB.\n"
        "MiGPT is designed for security, scalability, and production-ready deployment."
    ),
    version="1.0.0",
    contact={
        "name": "MiGPT Support",
        "email": "marvelousanyatonwu4@gmail.com",
    },
    license={"name": "MIT"},
    redoc_url=f"/api/{version}/redoc",
    docs_url=f"/api/{version}/docs",
    openapi_url=f"/api/{version}/openapi.json",
)


@app.get("/")
async def root():
    return {"message": "Hello MyGPT"}
