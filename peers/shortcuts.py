import json
from django.http import HttpResponse as DjangoHttpResponse


class HttpResponse(DjangoHttpResponse):
    """
    Custom Version of the HttpResponse, which automatically serializes Json objects.
    """

    def __init__(self, content=b'', *args, **kwargs):
        if isinstance(content, (dict, list, tuple)):
            content = json.dumps(content)

        super().__init__(content, *args, **kwargs)
