from django.shortcuts import render
from django.shortcuts import render
import numpy as np
from openai import OpenAI
from movie.models import Movie  # <- seguimos usando el modelo desde la app movie
from openai import OpenAI
from dotenv import load_dotenv
import io
import os


load_dotenv('./api_keys.env')
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend_movie(request):
    best_movie = None
    max_similarity = -1

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')

        # Generar embedding del prompt
        response = client.embeddings.create(
            input=[prompt],
            model="text-embedding-3-small"
        )
        prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

        # Buscar película más similar
        for movie in Movie.objects.all():
            if movie.emb:
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                similarity = cosine_similarity(prompt_emb, movie_emb)

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_movie = movie

    return render(request, "recommend.html", {
        "movie": best_movie,
        "similarity": round(float(max_similarity), 4) if best_movie else None
    })