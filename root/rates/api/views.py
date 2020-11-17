from django.conf import settings

from rest_framework import views, permissions
from rest_framework.response import Response

from .. import helpers


class RatesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        dof_rate = helpers.get_dof_rate()

        rates = {
            'rates': {
                'DOF': dof_rate,
            }
        }

        if settings.BANXICO_TOKEN:
            banxico_rate = helpers.get_banxico_rate()
            rates['rates']['Banxico'] = banxico_rate

        if settings.FIXER_TOKEN:
            fixer_rate = helpers.get_fixer_rate()
            rates['rates']['Fixer'] = fixer_rate

        return Response(rates)
