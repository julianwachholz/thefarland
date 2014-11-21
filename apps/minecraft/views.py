import json
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from vanilla import TemplateView
from .commands import query_player_coords
from .models import WebOperator


webop = TemplateView.as_view(template_name='minecraft/webop.html')
webop = permission_required('minecraft.is_op')(webop)

spectator = TemplateView.as_view(template_name='minecraft/spectator.html')
spectator = permission_required('minecraft.gamemode_spectator')(spectator)


@permission_required('minecraft.gamemode_spectator')
def gamemode_spectator(request):
    """
    Toggle between spectator and survival mode.

    """
    if request.method != 'POST':
        return JsonResponse({'status': 'FAIL', 'error': 'Use POST.'})

    try:
        webop = request.user.webop
    except WebOperator.DoesNotExist:
        return JsonResponse({'status': 'FAIL', 'error': 'You are not allowed to perform this action.'})

    if webop.is_spectator():
        webop.log_action('gamemode survival')
        coords = webop.get_coords()
        webop.go_survival()
        webop.tp(coords)
    else:
        coords = webop.query_coords(save=True)
        if coords is None:
            return JsonResponse({'status': 'FAIL', 'error': 'Player is not online.'})
        webop.log_action('gamemode spectator', json.dumps(coords, indent=2))
        webop.go_spectator()

    webop.save()

    return JsonResponse({
        'status': 'OK',
        'gamemode': webop.gamemode,
        'coords': coords,
    })
