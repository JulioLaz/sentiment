# from googletrans import Translator
from django.http import JsonResponse
from django.shortcuts import render
from sentiment_analyzer import SentimentAnalyzer  # Asegúrate de tener este archivo aquí


# analyzer = SentimentAnalyzer.load_model('sentiment_app/sentiment_model.pkl') C:\JulioPrograma\sentiment_project_amazon\sentiment_project_amazon\sentiment_project\sentiment_app\optimized_sentiment_model_2_10000.pkl
# analyzer = SentimentAnalyzer.load_model('myapp/optimized_sentiment_model_2_10000.pkl')

# def analyze_sentiment(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#         print(text)
#       #   translator = Translator()
#       #   translated_text = translator.translate(text, dest='en').text        
#       #   print(translated_text)
#         if text:
#             result = analyzer.predict(text)
#             return JsonResponse(result)
#     return render(request, 'sentiment_app/analyze.html')

from googletrans import Translator  # Asegúrate de tener esta biblioteca instalada
from django.http import JsonResponse
from django.shortcuts import render

# Cargar el modelo y su vocabulario
analyzer = SentimentAnalyzer.load_model('myapp/optimized_sentiment_model_2_10000.pkl')
vocab = analyzer.vectorizer.vocabulary_  # Obtiene el vocabulario del modelo cargado

# Función para analizar el sentimiento
def analyze_sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        print("Texto original:", text)
        
        # Traducción del texto al inglés
        translator = Translator()
        translated_text = translator.translate(text, dest='en').text
        print("Texto traducido:", translated_text)

        # Filtrar palabras según el vocabulario del modelo
        filtered_text = " ".join(
            word for word in translated_text.split() if word in vocab
        )
        print("Texto filtrado según vocabulario:", filtered_text)

        # Realizar la predicción si hay texto filtrado
        if filtered_text:
            result = analyzer.predict(filtered_text)
            return JsonResponse(result)
        else:
            return JsonResponse({
                'error': 'No valid words for prediction',
                'sentiment': 'unknown',
                'negative': None,
                'positive': None
            })

    return render(request, 'sentiment_app/analyze.html')
