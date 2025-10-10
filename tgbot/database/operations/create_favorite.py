from database.orm import AsyncSessionLocal
from database.models.favorite import FavoriteModel
from schemas.favorite_schema import FavoriteSchema

async def create_favorite(favorite_data: FavoriteSchema):
    async with AsyncSessionLocal() as session:
        favorite = FavoriteModel(
			id=favorite_data.id,
			user_id=favorite_data.user_id,
			resource_id=favorite_data.resource_id,
			added_at=favorite_data.added_at
		)
        session.add(favorite)
        await session.commit()