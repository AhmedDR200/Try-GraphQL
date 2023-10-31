import graphene
from graphene_django import DjangoObjectType
from .models import Books


class BookType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ('id', 'title', 'excerpt')


# Query for getting all books from the database
class Query(graphene.ObjectType):
    books = graphene.List(BookType)
    
    def resolve_books(self, info):
        return Books.objects.all()

    
schema = graphene.Schema(query=Query)


