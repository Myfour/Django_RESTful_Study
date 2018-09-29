import subprocess
from django.http import HttpResponse
from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSerializer, CodeListSerializer
from .models import Code
from rest_framework.authentication import SessionAuthentication


class APIRunCodeMixin(object):
    """
    运行代码操作
    """

    def run_code(self, code):
        try:
            subprocess.check_output(['python', '-c', code],
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True,
                                    timeout=30)
        except subprocess.CalledProcessError as e:
            output = e.output
        except subprocess.TimeoutExpired as e:
            output = '\r\n'.join(['Time Out!', e.output])
        return output


class CodeViewSet(APIRunCodeMixin, ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer

    def list(self, request, *args, **kwargs):
        serializer = CodeListSerializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         code = serializer.validated_data.get('code')
    #         serializer.save()
    #         if 'run' in request.query_params.keys():
    #             output = self.run_code(code)
    #             data = serializer.data
    #             data.update({'output': output})
    #             return Response(data=data, status=status.HTTP_201_CREATED)
    #         return Response(
    #             data=serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(
    #         data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.serializer_class(instance, data=request.data)
    #     if serializer.is_valid():
    #         code = serializer.validated_data.get('code')
    #         serializer.save()
    #         if 'run' in request.query_params.keys():
    #             output = self.run_code(code)
    #             data = serializer.data
    #             data.update({'output': output})
    #             return Response(data=data, status=status.HTTP_201_CREATED)
    #         return Response(
    #             data=serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.data, status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return self.run_create_or_update(request, serializer)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, request.data)
        return self.run_create_or_update(request, serializer)

    def run_create_or_update(self, request, serializer):
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            serializer.save()
            if 'run' in request.query_params.keys():
                output = self.run_code(code)
                data = serializer.data
                data.update({'output': output})
                return Response(data=data, status=status.HTTP_201_CREATED)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RunCodeAPIView(APIRunCodeMixin, APIView):
    def get(self, request, format=None):
        try:
            code = Code.objects.get(pk=request.query_params.get('id'))
        except models.ObjectDoesNotExist:
            return Response({
                'error': 'Object Not Found'
            },
                            status=status.HTTP_404_NOT_FOUND)
        output = self.run_code(code.code)
        return Response({'output': output}, status.HTTP_200_OK)


def home(request):
    with open('frontend/index.html', 'rb') as f:
        content = f.read()
    return HttpResponse(content)


def js(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        js_content = f.read()
    return HttpResponse(
        content=js_content, content_type='application/javascript')


def css(request, filename):
    with open('frontend/{}'.format(filename), 'rb') as f:
        css_content = f.read()
    return HttpResponse(content=css_content, content_type='text/css')


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    去除 CSRF 检查
    """

    def enforce_csrf(self, request):
        return