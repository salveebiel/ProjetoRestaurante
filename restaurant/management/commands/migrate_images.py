from django.core.management.base import BaseCommand
from restaurant.models import Prato
from cloudinary.uploader import upload
import os

class Command(BaseCommand):
    help = 'Migrate existing images to Cloudinary'

    def handle(self, *args, **options):
        for prato in Prato.objects.all():
            if prato.imagem and os.path.exists(prato.imagem.path):
                self.stdout.write(f'Migrating image for {prato.nome}...')
                try:
                    result = upload(prato.imagem.path, folder='pratos')
                    prato.imagem = result['public_id']
                    prato.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully migrated {prato.nome}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error migrating {prato.nome}: {e}'))
            else:
                self.stdout.write(f'No image or file not found for {prato.nome}')
