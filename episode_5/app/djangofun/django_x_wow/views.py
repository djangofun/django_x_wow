import json

from django.views.generic import TemplateView
from django.http import HttpResponse, Http404

from djangofun.django_x_wow.models import Character, SimcScore


class SimcScoresView(TemplateView):
    template_name = 'simc-scores.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SimcScoresView, self).get_context_data(**kwargs)
        region = kwargs.get('region')
        realm = kwargs.get('realm')
        name = kwargs.get('name')
        try:
            character = Character.objects.get(
                region__iexact=region,
                realm__iexact=realm,
                name__iexact=name,
            )
            result = []
            for simc_score in SimcScore.objects.filter(character=character).order_by('rating_time'):
                result.append({
                    'dps_score': simc_score.dps_score,
                    'rating_time': simc_score.rating_time.isoformat()
                })
            context['simc_scores'] = json.dumps(result)
            context['char_name'] = name
            return context
        except Character.DoesNotExist:
          raise Http404
