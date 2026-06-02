import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PrecosView(APIView):
    @swagger_auto_schema(
        operation_summary="Consultar preços de tapetes",
        operation_description=(
            "Busca os preços de tapetes na API externa Aladdin "
            "e retorna junto com a data informada pelo usuário."
        ),
        manual_parameters=[
            openapi.Parameter(
                name='data',
                in_=openapi.IN_QUERY,
                description='Data de consulta no formato YYYY-MM-DD (ex: 2025-06-01)',
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Dados retornados com sucesso",
                examples={
                    "application/json": {
                        "data_consulta": "2025-06-01",
                        "precos": []
                    }
                }
            ),
            400: "Parâmetro 'data' não informado",
            502: "API externa indisponível",
        }
    )
    def get(self, request: Request) -> Response:
        data_consulta: str | None = request.query_params.get('data')

        if not data_consulta:
            return Response(
                {"erro": "O parâmetro 'data' é obrigatório. Ex: ?data=2025-06-01"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resposta = requests.get(settings.ALADDIN_API_URL, timeout=10)
            resposta.raise_for_status()
            dados_externos: list = resposta.json()
        except requests.exceptions.ConnectionError:
            return Response(
                {"erro": "Não foi possível conectar à API externa. Tente novamente mais tarde."},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except requests.exceptions.Timeout:
            return Response(
                {"erro": "A API externa demorou muito para responder. Tente novamente."},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except requests.exceptions.HTTPError as e:
            return Response(
                {"erro": f"A API externa retornou um erro: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response({
            "data_consulta": data_consulta,
            "precos": dados_externos
        })