# django-hats
[![Coverage Status](https://coveralls.io/repos/github/GenePeeks/django-hats/badge.svg?branch=master)](https://coveralls.io/github/GenePeeks/django-hats?branch=master)
[![PyPI](https://img.shields.io/pypi/pyversions/django-hats.svg)]()

Role-based permissions system for Django. Everyone wears a different hat, some people wear multiple.

In a nutshell, django-hats is a reusable app, which doesn't try to re-invent the wheel by having Django Groups as its foundation. It provides a compact collection of easy to use patterns/utilities for role, and permission, based checks in CBVs and templates. They have the advantages of being: pragmatically defined, performant, clear syntax, and are well tested/documented!

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

Synchronize your database with defined roles:

```
python manage.py synchronize_roles
```

You're ready to go! Start defining permissions and securing your application!

## Working with roles

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

Then checking if a user has a role, or multiple roles:

```python
>>> from django_hats.utils import check_membership
>>> Scientist.check_membership(user)
True
>>> GeneticCounselor.check_membership(user)
False
>>> check_membership(user, Scientist)
True
>>> check_membership(user, [Scientist, GeneticCounselor])
False
>>> check_membership(user, [Scientist, GeneticCounselor], any=True)
True
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

## Mixins

Enforcing roles on the view:

```python
from django.views.generic import TemplateView
from django_hats.mixins import RoleRequiredMixin

from app.roles import GeneticCounselor, Scientist

class ProtectedGeneticReport(RoleRequiredMixin, TemplateView):
    role_required = GeneticCounselor
    template_name = 'template.html'


class ProtectedGeneticFiles(RoleRequiredMixin, TemplateView):
    # Works with existing Django `PermissionRequiredMixin`
    permission_required = ('change_subject', 'change_specimen')
    role_required = (GeneticCounselor, Scientist)
    role_required_any = True
    template_name = 'template.html'
```

## Templates

Checking roles in the template like permissions:  
**NOTE**: This is the reccomended way to check for roles in the template

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
**NOTE**: This works without the context processor, and is not required when using the context processor, if thats your thing

```
{% load roles %}

{% if user|has_role:'scientist' or user|has_role:genetic_counselor_role %}PROTECTED CONTENT!{% endif %}
```

## Signals

#### post_synchronize_roles
- `sender`: django-hats `AppConfig`


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
