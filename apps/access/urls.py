from django.urls import path

from apps.access.views import (
    AccessRuleDetailView,
    AccessRuleListCreateView,
    ResourceListCreateView,
    RoleListCreateView,
)

urlpatterns = [
    path("roles/", RoleListCreateView.as_view()),
    path("resources/", ResourceListCreateView.as_view()),
    path("rules/", AccessRuleListCreateView.as_view()),
    path("rules/<int:pk>/", AccessRuleDetailView.as_view()),
]
