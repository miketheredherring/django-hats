from django_hats.roles import Role


class Scientist(Role):
    class Meta:
        permissions = ('change_user', )


class GeneticCounselor(Role):
    pass


class BadlyNamedModel(Role):
    class Meta:
        name = 'GoodModelName'
