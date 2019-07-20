from allauth.socialaccount.models import *


def run():
    a = Site.objects.get(id=1)
    a.domain = "localhost"
    a.name = "hypertube"
    a.save()

    git = SocialApp.objects.filter(provider="github")
    if git.exists():
        pass
    else:
        git = SocialApp(provider="github",name="Github",client_id="",secret="")
        git.save()
        git.sites.add(1)
        git.save()

    ggl = SocialApp.objects.filter(provider="google")
    if ggl.exists():
        pass
    else:
        ggl = SocialApp(provider="google",name="Google_OAuth",client_id="",secret="")
        ggl.save()
        ggl.sites.add(1)
        ggl.save()