from dataclasses import dataclass, field
from typing import List

import pytest
from graphql import (
    ArgumentNode,
    EnumValueNode,
    FieldNode,
    FloatValueNode,
    IntValueNode,
    ListValueNode,
    NameNode,
    Node,
    ObjectFieldNode,
    ObjectValueNode,
    StringValueNode,
    VariableNode,
)

from camac.caluma import ast_utils


@dataclass
class FakeInfo:
    variable_values: dict
    field_nodes: List[Node] = field(default_factory=list)


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (IntValueNode(value=3), 3),
        (FloatValueNode(value=9.1), 9.10),
        (VariableNode(name=StringValueNode(value="foo")), "bar"),
        (StringValueNode(value="stringy"), "stringy"),
        (EnumValueNode(value=3), 3),  # yeah not really an enum
        (
            ListValueNode(
                values=[StringValueNode(value="one"), StringValueNode(value="two")]
            ),
            ["one", "two"],
        ),
        (
            ObjectValueNode(
                fields=[
                    ObjectFieldNode(
                        name=NameNode(value="one"),
                        value=StringValueNode(value="uno"),
                    ),
                    ObjectFieldNode(
                        name=NameNode(value="two"),
                        value=StringValueNode(value="dos"),
                    ),
                ]
            ),
            {"one": "uno", "two": "dos"},
        ),
    ],
)
def test_extract_node(input, expected_output):
    info = FakeInfo(variable_values={"foo": "bar"})
    out = ast_utils.extract_node(input, info)
    assert out == expected_output


def test_extract_filter_data():
    info = FakeInfo(
        variable_values={"foo": "bar"},
        field_nodes=[
            FieldNode(
                arguments=[
                    ArgumentNode(
                        name=NameNode(
                            value="filter",
                        ),
                        value=ListValueNode(
                            values=[
                                ObjectValueNode(
                                    fields=[
                                        ObjectFieldNode(
                                            name=NameNode(value="one"),
                                            value=StringValueNode(value="uno"),
                                        ),
                                        ObjectFieldNode(
                                            name=NameNode(value="two"),
                                            value=StringValueNode(value="dos"),
                                        ),
                                    ]
                                )
                            ]
                        ),
                    )
                ]
            )
        ],
    )

    out = ast_utils.extract_filter_data(info)
    assert out == [{"one": "uno", "two": "dos"}]
