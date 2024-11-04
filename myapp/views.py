from django.http import JsonResponse
from django.shortcuts import render
from sentiment_analyzer import SentimentAnalyzer  # Asegúrate de tener este archivo aquí


# analyzer = SentimentAnalyzer.load_model('sentiment_app/sentiment_model.pkl') C:\JulioPrograma\sentiment_project_amazon\sentiment_project_amazon\sentiment_project\sentiment_app\optimized_sentiment_model_2_10000.pkl
analyzer = SentimentAnalyzer.load_model('myapp/optimized_sentiment_model_2_10000.pkl')

def analyze_sentiment(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        print(text)
      #   translator = Translator()
      #   translated_text = translator.translate(text, dest='en').text        
      #   print(translated_text)
        if text:
            result = analyzer.predict(text)
            return JsonResponse(result)
    return render(request, 'sentiment_app/analyze.html')