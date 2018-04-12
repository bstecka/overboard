from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def default_questions_paginator(request, questions):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    return paginator.get_page(page)
