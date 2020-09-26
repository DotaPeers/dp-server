
def id_part_active(request):
    return {
        'id_active': False,
        'agent_connected': False,
        'user_id': request.session['userId'] if 'userId' in request.session else None,
    }
