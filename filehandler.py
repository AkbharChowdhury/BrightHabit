from django.core.files.storage import default_storage


class FileHandler:
    @staticmethod
    def profile_image_exists(image_path: str) -> bool:
        return default_storage.exists(f'profile_pics/{image_path}')

    @staticmethod
    def default_profile_image() -> str:
        return 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
