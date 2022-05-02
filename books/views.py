from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Book
from .forms import CommentForm


class BookListView(generic.ListView):
    model = Book
    paginate_by = 6
    template_name = 'books/book_list.html'
    context_object_name = 'books'


# class BookDetailView(generic.DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'

@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # get comment
    book_comments = book.comments.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        new_comment = comment_form.save(commit=False)
        new_comment.book = book
        new_comment.user = request.user
        new_comment.save()
        comment_form = CommentForm()
        return redirect('book_detail', pk=pk)

    else:
        comment_form = CommentForm()

    return render(request, 'books/book_detail.html',
                  {'book': book,
                   'comments': book_comments,
                   'comment_form': comment_form,
                   })


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'content', 'price', 'cover', ]
    template_name = 'books/book_create.html'


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'content', 'price', 'cover', ]
    template_name = 'books/book_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
