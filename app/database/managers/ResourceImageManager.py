from pydantic import UUID4
from sqlalchemy import select
from typing import List

from database.orm import AsyncSessionLocal
from schemas.resource_image_schema import ResourceImageWithoutResourceSchema, ResourceImageSchema
from database.models.resource_image import ResourceImageModel

class ResourceImageManager:
    @classmethod
    async def create(cls, resource_image_data: ResourceImageWithoutResourceSchema):
        async with AsyncSessionLocal() as session:
            resource_image = ResourceImageModel(**resource_image_data.model_dump())
            session.add(resource_image)
            await session.commit()
      
    @classmethod      
    async def delete(cls, resource_image_id: UUID4):
        async with AsyncSessionLocal() as session:
            statement = select(ResourceImageModel).where(ResourceImageModel.id == resource_image_id)
            favorite = (await session.execute(statement)).scalars().first()
            await session.delete(favorite)
            await session.commit()
                
    @classmethod
    async def get_one(cls, resource_image_id: UUID4) -> ResourceImageModel | None:
        async with AsyncSessionLocal() as session:
            statement = select(ResourceImageModel).where(ResourceImageModel.id == resource_image_id)
            resource_image = (await session.execute(statement)).scalars().first()
            
            if resource_image is None:
                return None    
            return ResourceImageSchema.model_validate(resource_image, from_attributes=True) \
                
    @classmethod
    async def get_many(cls, resource_id: UUID4) -> List[ResourceImageModel] | None:
        async with AsyncSessionLocal() as session:
            statement = select(ResourceImageModel).where(ResourceImageModel.resource_id == resource_id)
            resource_images = (await session.execute(statement)).scalars().all()
            
            if resource_images is None:
                return None    
            
            return [ResourceImageWithoutResourceSchema.model_validate(resource_image, from_attributes=True) for resource_image in resource_images]