from django.http import JsonResponse
import time

from . import helpers


def get_image_url(request, pk, uuid):
    """
    It receives image request and returns when it is ready.
    Makes 6 attempts with incremental intervals
    """
    sequence_verify = [1, 1, 2, 3, 5, 8, 13]
    verifications = 0
    while verifications < 7:
        response_data = helpers.get_url_momentum(uuid)
        if response_data:
            return JsonResponse(response_data)
        else:
            verifications += 1
            time.sleep(sequence_verify[verifications])