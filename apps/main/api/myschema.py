# from drf_spectacular.openapi import AutoSchema
#
# from drf_spectacular.utils import OpenApiParameter
#
# class CustomAutoSchema(AutoSchema):
#     # global_params = [
#     #     OpenApiParameter(
#     #         name = 'format',
#     #         type = str,
#     #         location = OpenApiParameter.QUERY,
#     #         default = 'json',
#     #         description = 'Формат запроса'
#     #     )
#     # ]
#
#     def get_override_parameters(self):
#         params = super().get_override_parameters()
#         return params
        # return params + self.global_params
