# django-hats
[![Coverage Status](https://coveralls.io/repos/github/GenePeeks/django-hats/badge.svg?branch=master)](https://coveralls.io/github/GenePeeks/django-hats?branch=master)

Role-based permissions system for Django. Everyone wears a different hat, some people wear multiple.

## Quick Start

Install with `pip`:

```
pip install git+git://github.com/GenePeeks/django-hats.git@v0.0.1
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

Assigning roles to a user(works with custom user models):

```python
>>> user = User.objects.first()
>>> Scientist.assign(user)
```

Then checking if a user has a role:

```python
>>> Scientist.check_membership(user)
True
>>> GeneticCounselor.check_membership(user)
False
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

Checking roles in the template with filter tag:

```
{% load roles %}

{% if user|has_role:'scientist' or user|has_role:genetic_counselor_role %}PROTECTED CONTENT!{% endif %}
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

Removing old roles/permissions from the database:

```
python manage.py synchronize_roles
```