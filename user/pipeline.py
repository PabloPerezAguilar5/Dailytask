from social_core.pipeline.user import get_username
from social_core.pipeline.social_auth import social_details

def save_google_profile_picture(strategy, details, response, user=None, *args, **kwargs):
    if user and response.get('picture'):
        user.google_profile_picture = response['picture']
        user.save()
    return {'user': user} 