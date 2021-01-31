from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from apps.videos.models import ApiKey


class AddApiKeyAPI(APIView):

    def post(self, request):
        response = {}
        data = request.data
        failed = []
        if data.get('reset'):
            ApiKey.objects.update(limit_exceeded=False, limit_exceeded_on=None)
            response['message'] = 'Api keys reset successful'

        for key in data.get('api_keys', []):
            obj, created = ApiKey.objects.get_or_create(api_key=key)
            if not created:
                failed.append('{}:Already exists'.format(key))

        if not failed:
            response['message'] = 'Api keys added successfully'
        else:
            response['failed'] = failed
        return JsonResponse(
            response,
            status=status.HTTP_200_OK
        )
