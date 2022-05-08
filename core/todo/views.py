from django.db.models import Q
from django.shortcuts import render
from .models import Identifier, Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from uuid import uuid4
# Create your views here.


class TodoAddView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            """
                Add Todo View
                route: base_url: /todo/add-todo/
                payloads: email, name, content
            """
            data = request.data
            email, name, content = data.get("email"), data.get("name"), data.get("content")

            email, created = Identifier.objects.get_or_create(email=email)

            if Task.objects.filter(name__iexact=name).exists():
                return Response({"detail": "TO-DO task already exist, how about you modify it."},
                                status=status.HTTP_400_BAD_REQUEST)

            task = Task.objects.create(slug=str(uuid4())[:10], email=email, name=name, content=content)

            return Response({"detail": f"{task.name} created", "data": TaskSerializer(task).data},
                            status=status.HTTP_201_CREATED)

        except (Exception, ) as err:
            return Response({"error-message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class TodoUpdateView(APIView):

    """
        Update Todo Task
        endpoint: base_url /todo/update-todo/<slug>/
        payload : name, content
    """
    permission_classes = []

    def put(self, request, slug=None):
        try:
            if slug is None:
                raise Exception("Todo Slug is Required in URL")

            data = request.data
            email, name, content, state = data.get("email"), data.get("name"), data.get("content"), data.get("state")

            task = Task.objects.get(slug=slug)

            if task.email.email != email:
                raise Exception("You are not allowed to Edit another User's Task")

            task.name, task.content = name, content
            if state.capitalize() not in ["Open", "Completed"]:
                raise Exception("The state of a Task can only be updated to Open or Completed")

            task.state = state.capitalize()
            task.save()

            return Response({"detail": "Updated Todo", "data": TaskSerializer(task).data},
                            status=status.HTTP_200_OK)

        except (Exception, ) as err:
            return Response({"error-message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class ListTask(APIView):

    """
        List out all TODO Task if `email` payload isn't provided.
        payload: email (required if you want to list user specific Tasks).
        endpoint: /todo/list/
    """
    permission_classes = []

    def get(self, request):
        try:
            data = request.data
            email = data.get("email", '')
            if not email:
                tasks = Task.objects.all()
                return Response({"detail": "List of TODO Task", "data": TaskSerializer(tasks, many=True).data},
                                status=status.HTTP_200_OK)

            field = Q("email__iexact")
            query_set = Task.objects.filter(email__email__iexact=email)

            if not query_set:
                return Response({"detail": "This User doesn't have any Task to-do."}, status=status.HTTP_200_OK)

            return Response({"detail": f"List of all TODO for User {email}", "data": TaskSerializer(query_set, many=True).data},
                            status=status.HTTP_200_OK)

        except (Exception, ) as err:
            return Response({"error-message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
