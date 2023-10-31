import graphene
from graphene_django.types import DjangoObjectType
from .models import Task

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, info):
        return Task.objects.all()

class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    task = graphene.Field(TaskType)

    def mutate(self, info, title, description, completed):
        task = Task(title=title, description=description, completed=completed)
        task.save()
        return CreateTask(task=task)


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    task = graphene.Field(TaskType)

    def mutate(self, info, id, title, description, completed):
        task = Task.objects.get(pk=id)
        if title is not None:  # Removed the extra "not" here
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        task.save()
        return UpdateTask(task=task)


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            task = Task.objects.get(pk=id)
            task.delete()
            return DeleteTask(success=True)
        except Task.DoesNotExist:
            return DeleteTask(success=False)


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
