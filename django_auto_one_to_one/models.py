from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User

def AutoOneToOneModel(parent, related_name=None, attr=None):
    """
    Class factory that returns an abstract model attached to a ``model`` object
    that creates and destroys concrete child instances where required.

        from django.db import models
        from django_auto_one_to_one import AutoOneToOneModel

        class Parent(models.model):
            parent_field = models.IntegerField(default=1)

        class Child(AutoOneToOneModel(Parent)):
            child_field = models.IntegerField(default=2)


        >>> p = Parent.objects.create()
        >>> p.child.child_field
        2
    """

    # Support string or classes for the parent
    if isinstance(parent, basestring):
        parent = models.get_model(*parent.split('.', 1))
        if parent is None:
            raise ValueError("Invalid model parent name")

    # Automatically work kkkkk
    if not attr:
        attr = parent._meta.verbose_name.replace(' ', '_')

    class Base(models.base.ModelBase):
        def __new__(mcs, name, bases, attrs):
            model = super(Base, mcs).__new__(mcs, name, bases, attrs)

            if model._meta.abstract:
                return model

            # Setup the signals that will automatically create and destroy
            # instances.
            #
            # We use weak=False or our receivers will be garbage collected.
            #
            def on_create(sender, instance, created, *args, **kwargs):
                if created:
                    model.objects.create(**{attr: instance})

            def on_delete(sender, instance, *args, **kwargs):
                model.objects.filter(pk=instance).delete()

            post_save.connect(on_create, sender=parent, weak=False)
            pre_delete.connect(on_delete, sender=parent, weak=False)

            return model

    class Parent(models.Model):
        locals()[attr] = models.OneToOneField(
            parent,
            primary_key=True,
            related_name=related_name,
        )

        __metaclass__ = Base

        class Meta:
            abstract = True

        def __unicode__(self):
            return u"%s=%s" % (attr, getattr(self, attr))

    return Parent

def PerUserData(related_name=None):
    return AutoOneToOneModel(User, related_name=related_name)
