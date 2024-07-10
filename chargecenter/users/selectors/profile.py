from chargecenter.users.models import BaseUser, Profile


def create_profile(user: BaseUser, bio: str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)


def get_profile(user: BaseUser) -> Profile:
    return Profile.objects.get(user=user)
