# django-hats
[![Coverage Status](https://coveralls.io/repos/github/GenePeeks/django-hats/badge.svg?branch=master)](https://coveralls.io/github/GenePeeks/django-hats?branch=master)

Role-based permissions system for Django. Everyone wears a different hat, some people wear multiple.


## Quick Start

Install with `pip`:

```
pip install django-hats
```

Or, getting the latest build:
```
pip install git+git://github.com/GenePeeks/django-hats.git@master
```

Add `django_hats` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'django_hats',
    ...
)
```

Create `roles.py` in any registered applications in your Django project:

```python
from django_hats.roles import Role

class Scientist(Role):
    class Meta:
        permissions = ('change_subject', 'change_specimen')

class GeneticCounselor(Role):
    pass
```

Pragmatically assigning/removing/viewing `Permission` to role:

```python
>>> Scientist.add_permissions(perm_1, perm_2, ...)
>>> GeneticCounselor.remove_permissions(perm_3)
>>> Scientist.get_permissions()
[<Permission 'change_subject'>, <Permission 'change_specimen'>]
```

Assigning/removing roles for a user(works with custom user models):

```python
>>> user = User.objects.first()
>>> Scientist.assign(user)
>>> Scientist.remove(user)
```

Then checking if a user has a role:

```python
>>> Scientist.check_membership(user)
True
>>> GeneticCounselor.check_membership(user)
False
```

List users with a given role:

```python
>>> Scientist.get_users()
[<User 'Mike Hearing'>, <User 'Scientist_1'>]
```

Retrieving roles pragmatically:

```python
>>> from django_hats.roles import RoleFinder
...
>>> RoleFinder.by_user(user)
[<class 'Scientist'>, ]
>>> RoleFinder.by_name('genetic_counselor')
<class 'GeneticCounselor'>
>>> RoleFinder.by_group(group)
<class 'Scientist'>
```

Enforcing roles on the view:

```python
from django.views.generic import TemplateView
from django_hats.mixins import RoleRequiredMixin

from app.roles import GeneticCounselor, Scientist

class ProtectedGeneticReport(RoleRequiredMixin, TemplateView):
    role_required = GeneticCounselor
    template_name = 'template.html'


class ProtectedGeneticFiles(RoleRequiredMixin, TemplateView):
    # Works with existing Django PermissionRequiredMixin
    permission_required = ('change_subject', 'change_specimen')
    role_required = (GeneticCounselor, Scientist)
    template_name = 'template.html'
```

Checking roles in the template like permissions:

settings.py
```
TEMPLATE_CONTEXT_PROCESSORS = (
    ...
    'django_hats.context_processors.roles',
    ...
)
```

template.html
```html
{% if roles.scientist %}PROTECTED CONTENT!{% endif %}

{% if roles.genetic_counselor %}NOTE: Class names are converted to snake_case if not specified in role.Meta.name{% endif %}
```

Checking roles in the template with filter tag:

```
{% load roles %}

{% if user|has_role:'scientist' or user|has_role:genetic_counselor_role %}PROTECTED CONTENT!{% endif %}
```

## Management Commands

Synchronize roles/permissions from the database:

```
python manage.py synchronize_roles
```

Migrate a role which the class name/name has changed:

```
python manage.py migrate_role --old=OldRoleClass --new=NewRoleClass
```

Remove old roles/permissions from the database(only post migration if a name change occured):

```
python manage.py cleanup_roles
```
