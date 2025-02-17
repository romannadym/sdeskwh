import json

from rest_framework import parsers

class NestedMultipartParser(parsers.MultiPartParser):
    def parse(self, stream, media_type = None, parser_context = None):
        result = super().parse(stream = stream, media_type = media_type, parser_context = parser_context)

        data = {}

        for key, value in result.data.items():
            if value:
                if '[' in value and ']' in value:
                    data[key] = json.loads(value)
                else:
                    data[key] = value
        return parsers.DataAndFiles(data, result.files)
