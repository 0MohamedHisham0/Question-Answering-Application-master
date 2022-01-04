import os, io
import errno
import urllib
import urllib.request
from time import sleep
import pandas as pd
from urllib.request import urlopen, Request
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from googlesearch import search
from cdqa.utils.converters import pdf_converter
from cdqa.utils.filters import filter_paragraphs
from cdqa.utils.download import download_model, download_bnpp_data
from cdqa.pipeline.cdqa_sklearn import QAPipeline
from cdqa.utils.download import download_model
from .models import Upload
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import generics, status, mixins


from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Upload
from .serializers import FileSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def search_view(request):
    print("before post ==========")
    answerlist = {}
    if request.POST:
        download_model(model='bert-squad_1.1', dir='./models')
        a = Upload.objects.all()
        x = a.first()
        print("=============================")
        p = x.file
        print(p)
        question = request.POST.get('question')
        print(request)
        # question = question.encode("utf-8")
        #question = "What is the cold dark misty world of the dead, ruled by the goddess Hel?"
        print(question)
        #for idx, url in enumerate(search(question, tld="com", num=10, stop=None, pause=2)):
        #    crawl_result(url, idx)
        # change path to pdfs folder
        df = pdf_converter(directory_path='./media')
        # print("after data frame", df)
        cdqa_pipeline = QAPipeline(reader='/models/distilbert_qa.joblib', max_df=1.0)
        print("first pipeline")
        cdqa_pipeline.fit_retriever(df=df)
        print("second pipeline")
        prediction = cdqa_pipeline.predict(question)
        print("s3ody##################################################################################################################################")
        data = {
            'answer': prediction[0]
        }
        answerlist = {
            'query': question,
            'answer': prediction[0],
            'title': prediction[1],
            'paragraph': prediction[2]
        }
        print("finish", data)
        print('query: {}'.format(question))
        print('answer: {}'.format(prediction[0]))
        print('title: {}'.format(prediction[1]))
        print('paragraph: {}'.format(prediction[2]))
        print()
        return Response(answerlist)
        #return JsonResponse(answerlist)

    return render(request, 'search.html')




class QA(generics.GenericAPIView):
    serializer_class = FileSerializer
    queryset = Upload.objects.all()
    answerlist = {}


    def post(self, request):
        pass



def crawl_result(url, idx):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html.parser')
        # change path to pdfs folder
        filename = "/path/to/pdfs/" + str(idx) + ".pdf"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(filename, 'w') as f:
            for line in bs.find_all('p')[:5]:
                f.write(line.text + '\n')
    except (urllib.error.HTTPError, AttributeError) as e:
        pass








#### sonyy API ########

# from django.shortcuts import render
# from rest_framework.parsers import FileUploadParser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from .models import Upload
# from .serializers import FileSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny

'''class FileUploadView(APIView):
    permission_classes = []
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        context = request.data.copy()
        context['file'] = request.FILES.get('file')

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((AllowAny,))
def all_files(request):
    if request.method == 'GET':
        qs = Upload.objects.all()
        s = FileSerializer(qs, many=True)
        return Response(data=s.data)
'''

##loayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy




####heroku config:set DISABLE_COLLECTSTATIC=1 --app blooming-tundra-42977