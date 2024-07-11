from chargecenter.users.models import BaseUser, SalesPerson


def create_salesperson(user: BaseUser, first_name: str, last_name: str):
    return SalesPerson.objects.create(user=user, first_name=first_name, last_name=last_name)
