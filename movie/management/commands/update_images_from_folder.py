import os
import unicodedata
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Asigna imágenes a las películas desde la carpeta media/movie/images/'

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'  
        updated_count = 0
        not_found = []

      
        def normalize(text):
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
            text = text.lower().strip()
            return text

        
        try:
            image_files = os.listdir(images_folder)
        except FileNotFoundError:
            self.stdout.write("❌ Error: La carpeta de imágenes no existe.")
            return

        normalized_images = {}
        for f in image_files:
            if f.endswith('.png'):
                name = f[2:-4]  
                normalized_images[normalize(name)] = f

   
        for movie in Movie.objects.all():
            normalized_title = normalize(movie.title)
            image_name = normalized_images.get(normalized_title)

            if image_name:
                movie.image = f'movie/images/{image_name}'  
                movie.save()
                updated_count += 1
                self.stdout.write(f"✅ Imagen asignada: {movie.title} -> {image_name}")
            else:
                not_found.append(movie.title)

        self.stdout.write(f"\n🎯 {updated_count} imágenes actualizadas.")
        if not_found:
            self.stdout.write("⚠️ No se encontró imagen para:")
            for title in not_found:
                self.stdout.write(f" - {title}")
