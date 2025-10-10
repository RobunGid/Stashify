from database.orm import AsyncSessionLocal
from database.models.favorite import FavoriteModel
from schemas.favorite_schema import FavoriteSchema

async def create_favorite(favorite_data: FavoriteSchema):
    async with AsyncSessionLocal() as session:
        favorite = FavoriteModel(**favorite_data.model_dump())
        print(favorite_data.model_dump(), 1923939293)
        session.add(favorite)
        await session.commit()