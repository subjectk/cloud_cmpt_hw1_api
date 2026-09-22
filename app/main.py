import asyncio
import random
import re

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class RandomPokemonResponse(BaseModel):
    id: int
    name: str
    image: str
    description: str


app = FastAPI(
    title="Cloud Computing HW1 API",
    description="FastAPI backend starter for the personal introduction project.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", tags=["기본"])
def read_root() -> dict[str, str]:
    return {"message": "FastAPI server is running"}


@app.get("/health", response_model=HealthResponse, tags=["기본"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="hw1-api")


@app.get(
    "/pokemon/random",
    response_model=RandomPokemonResponse,
    tags=["포켓몬"],
)
async def random_pokemon() -> RandomPokemonResponse:
    pokemon_id = random.randint(1, 1025)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            pokemon_response, species_response = await asyncio.gather(
                client.get(pokemon_url),
                client.get(species_url),
            )
            pokemon_response.raise_for_status()
            species_response.raise_for_status()
    except (httpx.HTTPError, httpx.TimeoutException) as error:
        raise HTTPException(
            status_code=502,
            detail="PokeAPI를 호출하지 못했습니다.",
        ) from error

    pokemon = pokemon_response.json()
    species = species_response.json()
    description = next(
        (
            entry["flavor_text"]
            for entry in species.get("flavor_text_entries", [])
            if entry.get("language", {}).get("name") == "en"
        ),
        "No description available.",
    )

    sprites = pokemon.get("sprites", {})
    official_artwork = sprites.get("other", {}).get("official-artwork", {})
    image = official_artwork.get("front_default") or sprites.get("front_default")

    return RandomPokemonResponse(
        id=pokemon["id"],
        name=pokemon["name"],
        image=image,
        description=re.sub(r"\s+", " ", description).strip(),
    )
