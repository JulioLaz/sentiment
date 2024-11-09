from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sentiment_analyzer import SentimentAnalyzer
from deep_translator import GoogleTranslator
# import langid
import gemini
# import time

analyzer = SentimentAnalyzer.load_model('myapp/optimized_sentiment_model_2_10000.pkl')
vocab = analyzer.vectorizer.vocabulary_  # Obtiene el vocabulario del modelo cargado

# Función para analizar el sentimiento
@csrf_exempt
def analyze_sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        # time.sleep(2)       
        # def idioma(palabra): 
        #     idioma, _ = langid.classify(palabra) 
        #     return idioma == 'en'
        # print("Texto original:", text)
        
        # Traducción del texto al inglés
        try:
            translated_text = GoogleTranslator(source='auto', target='es').translate(text)
            print(f"Translation translated_text: {translated_text}")
        except Exception as e:
            translated_text='Lo siento, tengo problemas para traducir este texto'

        ### ACTIVAR GEMINI ###
        # analyzer_gemini= '50% positive, 50% negative'
        # analyzer_gemini= 'Lo siento error'
        analyzer_gemini= gemini.chat(text)
        print('analyzer_gemini :',analyzer_gemini)
        # print("analyzer_gemini:", analyzer_gemini)

        # Filtrar palabras según el vocabulario del modelo
        filtered_text = " ".join(word for word in text.split() if word in vocab)
        # print("Texto filtrado según vocabulario:", filtered_text)
        
        none_gemini= True

        
        if ("positive" in analyzer_gemini) | ("negative" in analyzer_gemini):
        #   print("Gemini result: ", analyzer_gemini)
          parts = analyzer_gemini.split(',')
          positive_gemini = int(parts[0].split('%')[0].strip())
          negative_gemini= int(parts[1].split('%')[0].strip())
        #   print("Gemini result positive_gemini: ", positive_gemini)
        #   print("Gemini result negative_gemini: ", negative_gemini)
        else: 
            none_gemini= 'None'
            positive_gemini= 0
            negative_gemini= 0
            # negative_gemini =0
        # print('filtered_text: ',filtered_text)
        # print('filtered_text TYPE: ',type(filtered_text))
        # print('filtered_text LEN: ',len(filtered_text), 'type of len: ',type(len(filtered_text)) )
        # Realizar la predicción si hay texto filtrado
        if filtered_text:
            result = analyzer.predict(filtered_text)
            print('result: ',result)
            # print('result: ',result['sentiment'])
            response_data = {
                'filtered_text': filtered_text,
                'result': result,  # El resultado del análisis de sentimiento
                'positive_gemini': positive_gemini,  # Resultado de Gemini
                'negative_gemini': negative_gemini,
                'translated_text': translated_text,  # Resultado de Gemini
                'gemini_result': analyzer_gemini,
                'sentiment': 'unknown',
                'none_gemini':none_gemini
            }
            return JsonResponse(response_data)
        else:
            # print("Gemini result positive_gemini: ", positive_gemini)
            # print("Gemini result negative_gemini: ", negative_gemini)
            # print("analyzer_gemini: ", analyzer_gemini)
            result='none'
            print('result SIN TEXTO: ',result)
            return JsonResponse({
                'positive_gemini': positive_gemini,  # Resultado de Gemini
                'negative_gemini': negative_gemini,
                'result':False,
                'translated_text': translated_text,  # Resultado de Gemini
                'filtered_text': filtered_text,
                'error': 'No valid words for prediction',
                'sentiment': 'unknown',
                'positive': 0,
                'negative': 0,
                'gemini_result': analyzer_gemini,
                # 'none_gemini':none_gemini
            })
    return render(request, 'sentiment_app/analyze.html')