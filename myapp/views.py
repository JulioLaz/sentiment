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
        translated_text = translator.translate(text, dest='es').text
        print("Texto traducido:", translated_text)

        ### ACTIVAR GEMINI ###
        analyzer_gemini= '50% positive, 50% negative'
        # analyzer_gemini= gemini.chat(text) 
        print("analyzer_gemini:", analyzer_gemini)

        if "Lo siento" not in analyzer_gemini:
          print("Gemini result: ", analyzer_gemini)
        # Filtrar palabras según el vocabulario del modelo
        filtered_text = " ".join(word for word in text.split() if word in vocab)
        print("Texto filtrado según vocabulario:", filtered_text)
        
        none_gemini= True

        
        if "Lo siento" not in analyzer_gemini:
          print("Gemini result: ", analyzer_gemini)
          parts = analyzer_gemini.split(',')
          positive_gemini = int(parts[0].split('%')[0].strip())
          negative_gemini= int(parts[1].split('%')[0].strip())
          print("Gemini result positive_gemini: ", positive_gemini)
          print("Gemini result negative_gemini: ", negative_gemini)
        else: 
            none_gemini= 'None'
            # negative_gemini =0
        print('filtered_text: ',filtered_text)
        print('filtered_text TYPE: ',type(filtered_text))
        print('filtered_text LEN: ',len(filtered_text), 'type of len: ',type(len(filtered_text)) )
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
            print('result: ',result)
            return JsonResponse({
               'positive_gemini': positive_gemini,  # Resultado de Gemini
                'negative_gemini': negative_gemini,
               'result':result ,
                'translated_text': translated_text,  # Resultado de Gemini
                'filtered_text': filtered_text,
                'error': 'No valid words for prediction',
                'sentiment': 'unknown',
                'negative': None,
                'positive': None,
                'gemini_result': analyzer_gemini,
                # 'none_gemini':none_gemini
            })
        # Realizar la predicción si hay texto filtrado
        # if filtered_text:
        #     result = analyzer.predict(filtered_text)
        #     return JsonResponse(result),analyzer_gemini
        # else:
        #     return JsonResponse({
        #         'error': 'No valid words for prediction',
        #         'sentiment': 'unknown',
        #         'negative': None,
        #         'positive': None
        #     })

    return render(request, 'sentiment_app/analyze.html')


#########################################################################
# from django.http import JsonResponse
# from django.shortcuts import render
# from sentiment_analyzer import SentimentAnalyzer
# from googletrans import Translator
# import gemini

# analyzer = SentimentAnalyzer.load_model('myapp/optimized_sentiment_model_2_10000.pkl')
# vocab = analyzer.vectorizer.vocabulary_

# def analyze_sentiment(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '').strip()
        
#         if not text:
#             return JsonResponse({'error': 'No text provided for analysis'})

#         print("Texto original:", text)

#         # Traducción del texto al inglés
#         translator = Translator()
#         try:
#             translated_text = translator.translate(text, dest='en').text
#             print("Texto traducido:", translated_text)
#         except Exception as e:
#             print("Error en la traducción:", str(e))
#             return JsonResponse({'error': 'Translation failed', 'details': str(e)})

#         # Ejecutar Gemini
#         try:
#             # analyzer_gemini = gemini.chat(text)
#             analyzer_gemini= '50% positive, 50% negative'

#         except Exception as e:
#             analyzer_gemini = 'Error en Gemini'
#             print("Error en Gemini:", str(e))
        
#         # Manejo del resultado de Gemini
#         none_gemini = "Lo siento" in analyzer_gemini
#         positive_gemini, negative_gemini = None, None
#         if not none_gemini:
#             try:
#                 parts = analyzer_gemini.split(',')
#                 positive_gemini = int(parts[0].split('%')[0].strip())
#                 negative_gemini = int(parts[1].split('%')[0].strip())
#                 print("Gemini result positive:", positive_gemini)
#                 print("Gemini result negative:", negative_gemini)
#             except (IndexError, ValueError) as e:
#                 print("Error al procesar el resultado de Gemini:", str(e))
#                 none_gemini = True

#         # Filtrar palabras según el vocabulario del modelo
#         filtered_text = " ".join(word for word in text.split() if word in vocab)
#         print("Texto filtrado según vocabulario:", filtered_text)

#         # Verificación de texto filtrado y análisis de sentimiento
#         if filtered_text:
#             try:
#                 result = analyzer.predict(filtered_text)
#                 sentiment = result.get('sentiment', 'unknown')
#                 print('Sentiment result:', result)
#                 response_data = {
#                     'filtered_text': filtered_text,
#                     'result': result,
#                     'positive_gemini': positive_gemini,
#                     'negative_gemini': negative_gemini,
#                     'translated_text': translated_text,
#                     'gemini_result': analyzer_gemini,
#                     'sentiment': sentiment,
#                     'none_gemini': none_gemini
#                 }
#             except Exception as e:
#                 print("Error en el análisis de sentimiento:", str(e))
#                 return JsonResponse({'error': 'Sentiment analysis failed', 'details': str(e)})
#         else:
#             response_data = {
#                 'translated_text': translated_text,
#                 'filtered_text': filtered_text,
#                 'error': 'No valid words for prediction',
#                 'sentiment': 'unknown',
#                 'positive': None,
#                 'negative': None,
#                 'gemini_result': analyzer_gemini,
#                 'none_gemini': none_gemini
#             }
        
#         return JsonResponse(response_data)

#     return render(request, 'sentiment_app/analyze.html')
