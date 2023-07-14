from drf_yasg import openapi


get_task_response_schema = openapi.Schema(
    
    type=openapi.TYPE_OBJECT,
    properties={
        'type': openapi.Schema(type=openapi.TYPE_STRING),
        'id': openapi.Schema(type=openapi.TYPE_STRING),
        'attributes': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'priority': openapi.Schema(type=openapi.TYPE_INTEGER),
                'created': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'modified': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'task_name': openapi.Schema(type=openapi.TYPE_STRING),
                'task_description': openapi.Schema(type=openapi.TYPE_STRING),
                'task_due_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        'relationships': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_assignee': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                        ),
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                        ),
                    },
                ),
                'task_creator': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            },
        ),
    },
)


patch_task_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'task_assignee': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
        ),
        'priority': openapi.Schema(type=openapi.TYPE_INTEGER),
        'task_name': openapi.Schema(type=openapi.TYPE_STRING),
        'task_description': openapi.Schema(type=openapi.TYPE_STRING),
        'task_due_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    },
)


patch_task_update_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'data': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'result': openapi.Schema(type=openapi.TYPE_STRING),
                'updated_task': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'task_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'task_assignee': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        ),
                        'priority': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'created': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'modified': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'task_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'task_description': openapi.Schema(type=openapi.TYPE_STRING),
                        'task_due_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                        'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'task_creator': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
                'status_code': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    },
)


get_task_comment_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'data': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'id': openapi.Schema(type=openapi.TYPE_STRING),
                'attributes': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'comment_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'created': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'modified': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        'comment': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
                'relationships': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'task_id': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'data': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                ),
                            },
                        ),
                        'comment_creator': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'data': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    },
)


post_task_comment_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'task_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'comment': openapi.Schema(type=openapi.TYPE_STRING),
    },
)

post_task_comment_response_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "result": openapi.Schema(type=openapi.TYPE_STRING),
                        "created_task_comment": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "comment_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "task_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                "modified": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                "comment": openapi.Schema(type=openapi.TYPE_STRING),
                                "comment_creator": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "type": openapi.Schema(type=openapi.TYPE_STRING),
                                        "id": openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                ),
                            },
                        ),
                        "status_code": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                ),
            },
        )

patch_task_comment_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'comment': openapi.Schema(type=openapi.TYPE_STRING),
    },
)
