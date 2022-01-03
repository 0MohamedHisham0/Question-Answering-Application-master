## views
from cdqa.pipeline import QAPipeline
from cdqa.utils.converters import pdf_converter
from rest_framework.views import APIView

from .models import Upload
from .serializers import FileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics, status, mixins


@api_view(['GET'])
def file_list(request):
    all_files = Upload.objects.all()
    data = FileSerializer(all_files, many=True).data
    return Response({'data': data})


@api_view(['GET'])
def file(request, id):
    book = Upload.objects.get(id=id)
    data = FileSerializer(book).data
    return Response({'data': data})

@authentication_classes([])
@permission_classes([])
class FileListAPI(generics.ListAPIView):
    model = Upload
    queryset = Upload.objects.all()
    serializer_class = FileSerializer


class FileOperationAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    queryset = Upload.objects.all()
    lookup_field = 'id'


@authentication_classes([])
@permission_classes([])
class FileRetrieveAPI(generics.RetrieveAPIView):
    serializer_class = FileSerializer
    queryset = Upload.objects.all()
    lookup_field = 'id'


@authentication_classes([])
@permission_classes([])
class BookAddAPI(generics.CreateAPIView):
    serializer_class = FileSerializer
    queryset = Upload.objects.all()


@authentication_classes([])
@permission_classes([])
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = FileSerializer
    queryset = Upload.objects.all()

    # def post(self, request):
    #     return self.create(request)

    def get(self, request):
        if request.GET['question'] != "":
            question = request.GET['question']
            # question = request.data
            print(request)
            print("########################")
            print(question)

            # change path to pdfs folder
            df = pdf_converter(directory_path='./media')
            # print("after data frame", df)
            cdqa_pipeline = QAPipeline(reader='./models/distilbert_qa.joblib', max_df=1.0)
            print("first pipeline")
            cdqa_pipeline.fit_retriever(df=df)
            print("second pipeline")
            prediction = cdqa_pipeline.predict(question)
            print(
                "s3ody##################################################################################################################################")
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


# first branch