import pytest


@pytest.mark.parametrize(
    "factory_name, attr",
    [
        ("work_item_list_filter_preset_factory", "query_params"),
        ("instance_acl_factory", "metainfo"),
        ("gis_data_source_factory", "config"),
        ("communications_topic_factory", "involved_entities"),
    ],
)
def test_leaky_attributes(db, request, factory_name, attr, distribution_settings):
    """
    Ensure that dict and list attributes in factories are constructed correctly.

    In the model factories, dict and list literals must not be used as
    attribute values. This has the same reason as why those are forbidden to
    be used in default arguments for functions: It's too easy to modify them
    in place, which then leads to the value leaking into the next instance
    of the same test.
    """

    # Note: distribution_settings is required, as otherwise some factories
    # will just not work

    factory_fn = request.getfixturevalue(factory_name)

    i0 = factory_fn()
    i1 = factory_fn()

    i0_attr = getattr(i0, attr)
    i1_attr = getattr(i1, attr)

    i1_len_before = len(i1_attr)

    # Modify attribute in first instance ...
    if isinstance(i0_attr, dict):
        i0_attr.update(foo="bar")
    elif isinstance(i0_attr, list):
        i0_attr.append("blah")

    # ... And check if it's modified in second instance:
    # If attribute in instance 0 is modified (not replaced!)
    # then the attribute in instance 1 MUST NOT be changed
    assert len(i1_attr) == i1_len_before, (
        f"Factory leak for {factory_fn.__name__}.{attr}"
    )

    # Each instance's attribute must be a separate object.
    # We cannot allow subsequent factory calls to have the same
    # object as attribute.
    # This is kinda duplicated from the previous check: above,
    # we verify the attributes are *functionally* separated,
    # here we check the attribute value's identity.
    assert i0_attr is not i1_attr


def test_no_bare_mutable_attrs_in_factories(db, request):
    """Ensure no factory in Camac-NG has mutable attributes.

    Similar to the above test, we go through all (our) model
    factories and check that there is no dict or list literal
    in the factory definition, which could cause leakage.
    """
    # Experimental: This messes with pytest's interna, but it's readonly,
    # and I like to have full completeness checks here.

    factories_checked = []
    candidate_names = [
        fact
        for fact in request._fixturemanager._arg2fixturedefs.keys()
        if fact.endswith("_factory")
    ]

    for fact in candidate_names:
        try:
            factory_fn = request.getfixturevalue(fact)
            model = factory_fn._meta.model
        except AttributeError:
            # Not a model factory, skip
            continue
        except pytest.FixtureLookupError:  # pragma: no cover
            # Some factories, such as `appeal_deadline_factory`, are defined
            # local to their test modules. However, depending on hierarchy, they
            # might not be loadable here (but still visible). We just accept
            # that they are not loadable and carry on
            continue
        if not model.__module__.startswith("camac."):  # pragma: no cover
            # Not a camac model
            continue

        for name, val in vars(factory_fn).items():
            if name.startswith("_"):
                continue
            assert type(val) not in (list, dict), (
                f"{factory_fn.__name__}.{name} should be LazyFunction(...) instead"
            )
        factories_checked.append(factory_fn)

    # Just make sure we found all our factories. if it suddenly becomes
    # less than 100, we know the factory discovery isn't working anymore.
    # (Unless of course we clean up the models significantly, in which
    # case we can just decrease the number here)
    assert len(factories_checked) >= 100
