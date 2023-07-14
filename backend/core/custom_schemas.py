from drf_yasg import openapi

get_user_list_schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                        'attributes': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'role': openapi.Schema(type=openapi.TYPE_STRING),
                                'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                            },
                        ),
                    },
                )


error_403_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'errors': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'source': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'pointer': openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
    },
)


create_user_reponse_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'data': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'result': openapi.Schema(type=openapi.TYPE_STRING),
                'created_user': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'role': openapi.Schema(type=openapi.TYPE_STRING),
                        'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                    },
                ),
                'status_code': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    },
)


create_user_request_schema = user_creation_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'role': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
    },
)