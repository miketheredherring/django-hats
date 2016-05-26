from django_hats.roles import Role


class Scientist(Role):
    pass


class GeneticCounselor(Role):
    pass


class BadlyNamedModel(Role):
    class Meta:
        name = 'GoodModelName'
