from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Book
from .forms import UserCommentForm, AnonymousCommentForm


class BookListView(generic.ListView):
    queryset = Book.objects.order_by('-id')
    model = Book
    paginate_by = 6
    template_name = 'books/book_list.html'
    context_object_name = 'books'


# class BookDetailView(generic.DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    # book = get_object_or_404(Book, pk=pk)
    # # get comment
    # book_comments = book.comments.all()
    def get_form_class(self):
        user = self.request.user
        return UserCommentForm if user.is_authenticated else AnonymousCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_active=True)
        context['form'] = self.get_form_class()()
        return context

    def post(self, *args, **kwargs):
        request = self.request
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if isinstance(form, UserCommentForm):
                comment.user = request.user
            comment.book = self.get_object()
            comment.save()
            return redirect(comment.get_absolute_url())
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    # if request.method == "POST":
    #     comment_form = UserCommentForm(request.POST)
    #     new_comment = comment_form.save(commit=False)
    #     new_comment.book = book
    #     new_comment.user = request.user
    #     new_comment.save()
    #     comment_form = UserCommentForm()
    #     return redirect('book_detail', pk=pk)

    # else:
    #     comment_form = UserCommentForm()
    #
    # return render(request, 'books/book_detail.html',
    #               {'book': book,
    #                'comments': book_comments,
    #                'comment_form': comment_form,
    #                })


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'content', 'price', 'cover', ]
    template_name = 'books/book_create.html'

    def form_valid(self, form):
        book = form.save(commit=False)
        book.user = self.request.user
        book.save()
        return redirect(book.get_absolute_url())


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
