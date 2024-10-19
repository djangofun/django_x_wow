from django.urls import path

from djangofun.django_x_wow.views import SimcScoresView


urlpatterns = [
    path("simc-scores/<str:region>/<str:realm>/<str:name>/", SimcScoresView.as_view()),
]

