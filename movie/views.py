import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.shortcuts import render
from django.http import HttpResponse
from collections import Counter



from .models import Movie

# Create your views here.
def home (request):
    #return HttpResponse ('<h1>Welcome to Home page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Camilo Salazar'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm , 'movies': movies})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat= True).distinct().order_by('year')

    movie_counts_by_year = {} # Crear un diccionario para almacenar la cantidad de películas por año
    for year in years: # Contar la cantidad de películas por año
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5 # Ancho de las barras
    bar_spacing = 0.5 # Separación entre las barras
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    genres = Movie.objects.values_list('genre', flat=True)

    movie_counts_by_genre = {}  
    for genre in genres:
        if genre:  # Si el género no es None o vacío
            first_word = genre.split()[0]  # Tomar la primera palabra
        else:
            first_word = "Unknown"  

        if first_word in movie_counts_by_genre:
            movie_counts_by_genre[first_word] += 1
        else:
            movie_counts_by_genre[first_word] = 1

    bar_width = 0.5 # Ancho de las barras
    bar_spacing = 0.5 # Separación entre las barras
    bar_positions = range(len(movie_counts_by_genre)) # Posiciones de las barras

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png)
    graphic2 = graphic2.decode('utf-8')
    

    return render(request, 'statistics.html', {'graphic': graphic, 'graphic2': graphic2})


def about (request):
    return render (request, 'about.html', {'name':'Camilo Salazar'})
 