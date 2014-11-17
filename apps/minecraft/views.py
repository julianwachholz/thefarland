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
def get_coords(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'FAIL', 'error': 'Use POST.'})

    coords = query_player_coords(request.user.username)
    if coords is None:
        return JsonResponse({'status': 'FAIL', 'error': 'Player not found.'})

    coords.update({
        'status': 'OK',
    })

    WebOperator.objects.filter(user=request.user).update(
        last_x=coords['x'],
        last_y=coords['y'],
        last_z=coords['z'],
    )
    return JsonResponse(coords)
