from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class Genre(models.Model):
    """
    Модель, представляющая книжный жанр (например, научную фантастику, нон-фикшн).
    """
    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self):
        """
        Строка для представления объекта модели (на сайте администратора и т.д.с)
        """
        return self.name


class Publisher(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Введите название издания (например, Penguin Classics, Альфа-книга)"
    )
    publication_city = models.CharField(
        max_length=100,
        help_text="Введите город выпуска издания (например, Москва, Нью-Йорк)"
    )


    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретному экземпляру издания."""
        return reverse('publisher-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    модель книги
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    """
    # Используется внешний ключ(ForeignKey), потому что у книги может быть только один автор, но у авторов может быть несколько книг
    # Автор в виде строки, а не объекта, поскольку он еще не был объявлен в файле.
    """
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    publishers = models.ManyToManyField(Publisher, related_name='books')


    """
    # ManyToManyField(многие ко многим) используется потому, что жанр может содержать много книг. Книги могут охватывать много жанров.
    # Класс жанра уже определен, поэтому мы можем указать объект, указанный выше.
    """

    def __str__(self):
        """
        Строка для представления модельного объекта.
        """
        return self.title


    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Модель, представляющая конкретный экземпляр книги (т.е. ту, которую можно взять напрокат в библиотеке).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')


    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        """
        Строка для представления модельного объекта.
        """
        return '%s (%s)' % (self.id,self.book.title)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    модель автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному автору книги.
        """
        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):
        """
        Строка для представления модельного объекта.
        """
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


