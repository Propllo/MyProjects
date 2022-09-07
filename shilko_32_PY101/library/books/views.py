from django.shortcuts import render
from .models import Books


def books_index(request):
    book_info = Books.objects.all()
    context = {
        'books': book_info
    }
    return render(request, 'books_index.html', context)


def books_detail(request, pk):
    book_info = Books.objects.get(pk=pk)
    context = {
        'books': book_info
    }
    return render(request, 'books_detail.html', context)

