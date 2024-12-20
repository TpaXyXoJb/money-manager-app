from drf_yasg import openapi

swagger_category_viewset = {
    'operation_description': 'Managing categories (Create, Retrieve, Delete)',
}

swagger_all_categories_info = {
    'operation_description': 'Get the transaction summary for the category',
    'methods': ['GET', ],
    'responses': {
        200: openapi.Response(
            description="Category list including transaction's sum",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
                        'category_type': openapi.Schema(type=openapi.TYPE_STRING,
                                                        description='Category type (Income/Expense)'),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Transaction sum in category')
                    }
                )
            )
        )
    }
}

swagger_transaction_viewset = {
    'operation_description': 'Managing transactions (Create, Retrieve, Update, Delete)',
}

swagger_transaction_global_info = {
    'operation_description': 'Get the transaction summary for income and expense',
    'methods': ['GET', ],
    'responses': {
        200: openapi.Response(
            description="Summary of income and expense",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'income': openapi.Schema(type=openapi.TYPE_NUMBER, description='Income sum'),
                        'expense': openapi.Schema(type=openapi.TYPE_NUMBER, description='Expense sum'),
                    }
                )
            )
        )
    }
}

swagger_widget_viewset = {
    'operation_description': 'Managing widgets (Create, Retrieve, Delete)',
    'responses': {
        200: openapi.Response(
            description="Widget list including transaction's sum",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Widget ID'),
                        'limit': openapi.Schema(type=openapi.TYPE_NUMBER, description='Limit for expense'),
                        'criterion': openapi.Schema(type=openapi.TYPE_STRING, description='Criterion (greater/less)'),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Transaction sum in category')
                    }
                )
            )
        )
    }
}
