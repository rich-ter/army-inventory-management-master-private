from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def url(self, name, *args, **kwargs):
        try:
            url = super().url(name, *args, **kwargs)
        except ValueError:
            # If the file is missing, use a default font URL or return a generic URL
            url = '/static/fonts/default-font.woff2'  # Adjust this to your needs
        return url

    def post_process(self, *args, **kwargs):
        try:
            return super().post_process(*args, **kwargs)
        except ValueError as e:
            # Log the error or handle it as needed
            self.logger.warning(f"File not found during post_process: {e}")
            return []
