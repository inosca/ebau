# Permissions module - Use cases

This chapter is intended to document how common situations can be implemented using
the new permissions module. We use some explicit, actual examples from the current
system[^1].


[^1]: Of course, we'll need to reword this once the module becomes active, as it won't
make sense to explain what we're doing in terms of what the old system did... 

## The Instance Queryset Mixin

The `InstanceQuerysetMixin` uses the `@permission_aware` decorator and it's associated magic
to decide who gets to see which instances (dossiers).

### Old behaviour

Depending on the user's active role (selected via optional `X-Camac-Group` HTTP header),
various more-or-less complex implementations of the `get_queryset()` method are called.

### New behaviour

For compatibility across all viewsets currently in the code base, the
mixin should be kapt around. However, the `get_queryset()` method won't use
the `@permission_aware` decorator anymore. Instead, it will use the new permission module's
simple filtering API:

```python
    def get_queryset(self, group=None):
        queryset = self.get_base_queryset()
        # Potentially, we'd also need a group override in the `filter_queryset()`,
        # but that's easy to add
        queryset = permisisons.filter_queryset(queryset, user=self.context.user)
        return queryset
```


## The Instance Editable mixin

The `InstanceEditableMixin` is used to decide whether a certain operation
is allowed on an instance (or related object).

### Old behaviour

It applies the same `@permission_aware` decorator, and within each
variant, applies different rules to decide which permissions are currently
applicable for the user.

The whole implementation of the `get_editable()` method and it's
role-dependent variants spans roughly 60 lines of Python code.

### New behaviour

With the new permissions subsystem, no checking depending on user's active
role or relationship to the case is required:

```python
  def get_editable(self, instance):
      return permissions.get_permissions(instance=instance, user=self.request.user)
```
