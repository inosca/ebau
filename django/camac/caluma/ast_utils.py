from functools import singledispatch

from graphql import (
    EnumValueNode,
    ListValueNode,
    ObjectValueNode,
    ValueNode,
    VariableNode,
)

"""
Generic utilities for dealing with Caluma GraphQL ASTs.

Provide functions to extract information from a GQL query.
Particularly, there are two useful things here as of now:

* `extract_case_from_filters()` to get filter data identifying a case or instance
* `extract_node()` to get a dict/list representation of any node
"""

# TODO: This should be moved to Caluma core once we have a usable and stable set
# of functions here. The current state is rather single-purpose, but due to the
# general usefulness of extracting data from the GQL abstract syntax tree, we
# should keep in mind to publish this to Caluma once it's mature enough


def extract_case_from_filters(info):
    """Return case info from GQL filters, if any.

    Return either a ('case_id', ...) tuple, a ('instance_id', ...)
    tuple, or None, depending on whether a "compatible" filter was
    passed in the GQL query.
    """

    # Note: We only return something IFF we can positively identify
    # a case or an instance. Any filter that may also apply to
    # work items is ignored, as then we would also need to check the
    # node types as well, causing a lot more code. TODO: This may be
    # a useful development in the future, but now we're interested in
    # low-hanging fruit

    # Also note: depending on how the filters are parametrized, Graphene
    # translates them to snake_case (If the whole filter comes as a single
    # variable, the keys are translated, but if only some part of the filter
    # value is a variable, the node names correspond to the schema's view and
    # therefore are camelCase)
    case_filters = ["case", "rootCase", "caseFamily", "root_case", "case_family"]
    meta_filters = [
        "rootCaseMetaValue",
        "root_case_meta_value",
        "metaValue",
        "meta_value",
        "caseMetaValue",
        "case_meta_value",
    ]

    filter_data = extract_filter_data(info)
    for filter in filter_data:
        # meta filters are of structure:
        # filtername: {key: something, value: something_else} or
        # filtername: [{key: something, value: something_else}]
        for f_name in meta_filters:
            arg = filter.get(f_name)
            if not arg:
                continue

            if isinstance(arg, dict):
                arg = [arg]

            if _match := next(
                (obj for obj in arg if obj["key"] == "camac-instance-id")
            ):
                return ("instance_id", _match["value"])

        # case filters are of structure:
        # filtername: id_value
        for f_name in case_filters:
            if arg := filter.get(f_name):
                return ("case_id", arg)

    # simplify call-site by always returning a 2-tuple
    return None, None


def extract_filter_data(info) -> list:
    for node in info.field_nodes:
        for arg in node.arguments:
            if arg.name.value == "filter":
                return extract_node(arg.value, info)
    return []


@singledispatch
def extract_node(node, info):  # pragma: no cover
    """Turn the given node into a dict/list structure.

    Not only is the AST turned into a more easily inspectable
    dict/list structure, but any variable references are de-referenced and
    inlined, so the return structure can be dealt with directly.
    """
    ...


@extract_node.register
def _(node: VariableNode, info):
    return info.variable_values[node.name.value]


@extract_node.register
def _(node: ListValueNode, info):
    return [extract_node(sub, info) for sub in node.values]


@extract_node.register
def _(node: ObjectValueNode, info):
    return {sub.name.value: extract_node(sub.value, info) for sub in node.fields}


@extract_node.register
def _(node: EnumValueNode, info):
    return node.value


@extract_node.register
def _(node: ValueNode, info):
    return node.value
