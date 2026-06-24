from django.shortcuts import render

from .models import PolicyChallenge, PolicyFramework


def policy_index(request):
    frameworks = PolicyFramework.objects.all()
    challenges = PolicyChallenge.objects.all()
    return render(
        request,
        "policy/index.html",
        {"frameworks": frameworks, "challenges": challenges},
    )
