from io import BytesIO

from .s3_base import S3Client


class S3Users(S3Client):
    async def upload_image(self, user_id: int, image: BytesIO) -> str:
        path = f'/avatars/{user_id}.webp'
        await self.upload_file(path, 'images', image)
        return path

    async def get_image(self, path: str) -> BytesIO:
        return await self.get_file(path, 'images')
