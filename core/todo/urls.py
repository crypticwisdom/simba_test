from django.urls import path
from .views import TodoAddView, TodoUpdateView, ListTask

urlpatterns = [
    path("add-todo/", TodoAddView.as_view(), name="add-todo"),
    path("update-todo/<slug:slug>/", TodoUpdateView.as_view(), name="update-todo"),
    path("update-todo/", TodoUpdateView.as_view()),
    path("list/", ListTask.as_view()),

]