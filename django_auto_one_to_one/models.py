from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth import get_user_model
from django.apps import apps


def AutoOneToOneModel(parent, related_name=None, attr=None, on_delete=models.CASCADE, auto=True):
    """
    Automatically create child model instances when a parent class is created.

    For example, given the following model definition::

        from django.db import models
        from django_auto_one_to_one import AutoOneToOneModel

        class Parent(models.Model):
            field_a = models.IntegerField(default=1)

        class Child(AutoOneToOneModel(Parent)):
            field_b = models.IntegerField(default=2)

    ... creating a ``Parent`` instance automatically creates a related
    ``Child`` instance::

        >>> p = Parent.objects.create()
        >>> p.child
        <Child: parent=assd>
        >>> p.child.field_b
        2

    You must ensure that child models can be created without arguments via
    ``default=`` rather than overriding ``save``.

    Related names
    =============

    You can specify the related name on the parent via ``related_name``. The
    default is to use Django's default ``related_name`` logic, often resulting
    in clunky English or a clunky cross-app API:

        class UserData(AutoOneToOneModel('auth.User'), related_name='profile'):
            field_d = models.IntegerField(default=4)

        >>> u = User.objects.create_user(...)
        >>> u.profile.field_d
        4


    Custom field names
    ==================

    You can also specify the attribute or field name that is added to the child
    class. The default is to use a name based on the parent class name::

        class Child3(AutoOneToOneModel(Parent):
            field_e = models.IntegerField(default=5)

        >>> p = Parent.objects.create()
        >>> p.child.parent == p
        True

    However, you can specify a custom attribute via ``attr``:

        class Child2(AutoOneToOneModel(Parent, attr='custom_parent_name'):
            field_f = models.IntegerField(default=6)

        >>> = Parent.objects.create()
        >>> p.child.custom_parent_name == p
        True

    Convenience classes
    ===================

    As a convenience method, ``PerUserData`` will create instances hanging off
    the default Django ``User`` class.

        class Profile(PerUserData('profile')):
            nickname = models.CharField(max_length=40)
    """

    # Automatically calculate attribute on child class
    if not attr:
        attr = parent._meta.verbose_name_raw.replace(' ', '_')

    # The current implementation is a class factory that returns an abstract
    # parent model. It's a little convoluted but I'm not sure everything is
    # setup enough in a class decorator.
    class Base(models.base.ModelBase):
        def __new__(mcs, name, bases, attrs):
            model = super(Base, mcs).__new__(mcs, name, bases, attrs)

            if model._meta.abstract:
                return model

            # Avoid virtual models (for, for instance, deferred fields)
            if model._meta.concrete_model is not model:
                return model

            if not auto:
                return model
            
            # Don't set up signals for models that aren't installed as the
            # database tables won't exist.
            try:
                apps.get_app_config(model._meta.app_label)
            except LookupError:
                return model

            # Setup the signals that will automatically create and destroy
            # instances.
            #
            # We use weak=False or our (inline) receivers will be garbage
            # collected.
            def on_create_cb(sender, instance, created, *args, **kwargs):
                if created:
                    model.objects.create(**{attr: instance})

            def on_delete_cb(sender, instance, *args, **kwargs):
                model.objects.filter(pk=instance).delete()

            post_save.connect(on_create_cb, sender=parent, weak=False)
            pre_delete.connect(on_delete_cb, sender=parent, weak=False)

            return model

    class Parent(models.Model, metaclass=Base):
        locals()[attr] = models.OneToOneField(
            parent,
            on_delete=on_delete,
            primary_key=True,
            related_name=related_name,
        )

        class Meta:
            abstract = True

        def __str__(self):
            return "{}={}".format(attr, getattr(self, attr))

    return Parent


def PerUserData(*args, **kwargs):
    return AutoOneToOneModel(get_user_model(), *args, **kwargs)
