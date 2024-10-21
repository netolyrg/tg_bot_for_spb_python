from django.core.management.base import BaseCommand

from core.tg import get_app


class Command(BaseCommand):
    help = 'Bot polling'

    def handle(self, *args, **options):
        app = get_app()
        app.run_polling()
