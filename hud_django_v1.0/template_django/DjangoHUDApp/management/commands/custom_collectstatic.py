from django.core.management.base import BaseCommand
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand
from whitenoise.storage import MissingFileError

class Command(BaseCommand):
    help = 'Collect static files, ignoring missing files.'

    def add_arguments(self, parser):
        CollectStaticCommand.add_arguments(self, parser)

    def handle(self, *args, **options):
        try:
            collectstatic_command = CollectStaticCommand()
            collectstatic_command.handle(*args, **options)
        except MissingFileError as e:
            self.stdout.write(self.style.WARNING(f"Warning: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
