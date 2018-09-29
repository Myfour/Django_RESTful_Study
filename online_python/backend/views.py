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

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            serializer.save()
            if 'run' in request.query_params.keys():
                output = self.run_code(code)
                data = serializer.data
                data.update({'output': output})
                return Response(data=data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.data)
        return Response
