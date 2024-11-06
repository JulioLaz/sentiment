from django.http import JsonResponse
from django.shortcuts import render
from sentiment_analyzer import SentimentAnalyzer  # Asegúrate de tener este archivo aquí
from googletrans import Translator  # Asegúrate de tener esta biblioteca instalada
import gemini

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
        analizer_gemini= gemini.chat(translated_text)
        print("Texto traducido:", translated_text)

        # Filtrar palabras según el vocabulario del modelo
        filtered_text = " ".join(
            word for word in translated_text.split() if word in vocab
        )
        print("Texto filtrado según vocabulario:", filtered_text)
        print("Gemini result: ", analizer_gemini)


        # Realizar la predicción si hay texto filtrado
        if filtered_text:
            result = analyzer.predict(filtered_text)
            response_data = {
                'result': result,  # El resultado del análisis de sentimiento
                'gemini_result': analizer_gemini  # Resultado de Gemini
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({
                'error': 'No valid words for prediction',
                'sentiment': 'unknown',
                'negative': None,
                'positive': None,
                'gemini_result': analizer_gemini  # Añadir resultado de Gemini incluso en este caso
            })
        # Realizar la predicción si hay texto filtrado
        # if filtered_text:
        #     result = analyzer.predict(filtered_text)
        #     return JsonResponse(result),analizer_gemini
        # else:
        #     return JsonResponse({
        #         'error': 'No valid words for prediction',
        #         'sentiment': 'unknown',
        #         'negative': None,
        #         'positive': None
        #     })

    return render(request, 'sentiment_app/analyze.html')
