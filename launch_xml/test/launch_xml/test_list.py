# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test parsing list attributes."""

import io
import textwrap
from typing import List

from launch import LaunchContext
from launch.utilities.type_utils import perform_typed_substitution

from parser_no_extensions import load_no_extensions


def test_list():
    """Parse tags with list attributes."""
    xml_file = \
        """\
        <root>
            <tag attr="1,2,3" attr-sep=","/>
            <tag attr="1 2 3" attr-sep=" "/>
            <tag attr="1, 2, 3" attr-sep=", "/>
        </root>
        """
    xml_file = textwrap.dedent(xml_file)
    root_entity, parser = load_no_extensions(io.StringIO(xml_file))
    tags = root_entity.children
    assert tags[0].get_attr('attr', data_type=List[str]) == ['1', '2', '3']
    assert tags[0].get_attr('attr', data_type=List[int]) == [1, 2, 3]
    assert tags[0].get_attr('attr', data_type=List[float]) == [1., 2., 3.]


def test_list_with_substitution():
    """Resolve a substituted list after applying the XML separator."""
    xml_file = \
        """\
        <root>
            <tag attr="$(var int_array)" attr-sep=","/>
        </root>
        """
    xml_file = textwrap.dedent(xml_file)
    root_entity, parser = load_no_extensions(io.StringIO(xml_file))
    tag = root_entity.children[0]

    value = tag.get_attr('attr', data_type=List[int], can_be_str=True)
    normalized_value = parser.parse_if_substitutions(value)

    context = LaunchContext()
    context.launch_configurations['int_array'] = '1,2,3'
    assert perform_typed_substitution(context, normalized_value, List[int]) == [1, 2, 3]


if __name__ == '__main__':
    test_list()
