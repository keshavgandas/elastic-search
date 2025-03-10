from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Q
from .documents import ProductDocument
from django.shortcuts import render

class ProductAPI(APIView):
    def get(self, request):
        query = request.GET.get('q', '')

        # Construct search query
        if query:
            q = Q(
                'multi_match',
                query=query,
                fields=['product_name', 'brand'],
                fuzziness='AUTO',
                operator='and'
            )
            search = ProductDocument.search().query(q)
        else:
            search = ProductDocument.search()

        # Execute search with error handling
        try:
            response = search.execute()
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        # Extract results
        results = [hit.to_dict() for hit in response]
        return Response({"results": results})

def index(request):
    return render(request, 'index.html')


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination
# from elasticsearch_dsl import Q
# from .documents import ProductDocument
# from django.shortcuts import render

# class ProductPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# class ProductAPI(APIView):
#     pagination_class = ProductPagination

#     def get(self, request):
#         query = request.GET.get('q', '')
#         page_size = int(request.GET.get('page_size', 10))

#         # Construct search query
#         if query:
#             q = Q(
#                 'multi_match',
#                 query=query,
#                 fields=['product_name', 'brand'],
#                 fuzziness='AUTO',
#                 operator='and'
#             )
#             search = ProductDocument.search().query(q)
#         else:
#             search = ProductDocument.search()

#         # Implement pagination by slicing the search object
#         paginator = self.pagination_class()
#         start = (paginator.page.number - 1) * paginator.page_size
#         end = paginator.page.number * paginator.page_size
#         search = search[start:end]

#         # Execute search with error handling
#         try:
#             response = search.execute()
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

#         # Extract results
#         results = [hit.to_dict() for hit in response]
#         return paginator.get_paginated_response(results)

# def index(request):
#     return render(request, 'index.html')
