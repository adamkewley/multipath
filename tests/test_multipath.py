# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import tempfile
from unittest import TestCase

import os

import multipath


class TestMultipath(TestCase):

    def test_join_returns_expected_result_for_nominal_case(self):
        first = "/some/dir"
        input_dirs = [
            first,
            "/another/dir",
            "a/third/dir",
        ]
        returned_path = multipath.join(input_dirs, "sub1", "sub2")
        self.assertEqual(returned_path, os.path.join(first, "sub1", "sub2"))

    def test_join_raises_a_ValueError_if_input_dirs_is_empty(self):
        with self.assertRaises(ValueError):
            multipath.join([], "ignored", "args")

    def test_join_returns_expected_result_in_multiple_cases(self):
        dir1 = "/some/dir"
        dir2 = "/another/dir"
        dir3 = "a/relative/dir"

        frag1 = "sub1"
        frag2 = "sub2"

        cases = [
            ([dir1], [], dir1),
            ([dir1], [frag1], os.path.join(dir1, frag1)),
            ([dir2, dir1], [frag1], os.path.join(dir2, frag1)),
            ([dir1, dir2, dir3], [frag1], os.path.join(dir1, frag1)),
            ([dir3], [], dir3),
            ([dir1, dir2], [frag2, frag1], os.path.join(dir1, frag2, frag1)),
        ]

        for dirs, paths, expected_output in cases:
            actual_output = multipath.join(dirs, *paths)
            self.assertEqual(expected_output, actual_output)

    def test_try_join_returns_expected_result_for_nominal_case(self):
        first = "/some/dir"
        input_dirs = [
            first,
            "/another/dir",
            "a/third/dir",
        ]
        returned_path = multipath.try_join(input_dirs, "sub1", "sub2")
        self.assertEqual(returned_path, os.path.join(first, "sub1", "sub2"))

    def test_try_join_returns_None_if_input_dirs_is_empty(self):
        self.assertIsNone(multipath.try_join([], "ignored", "args"))

    def test_try_join_returns_expected_result_in_multiple_cases(self):
        dir1 = "/some/dir"
        dir2 = "/another/dir"
        dir3 = "a/relative/dir"

        frag1 = "sub1"
        frag2 = "sub2"

        cases = [
            ([dir1], [], dir1),
            ([dir1], [frag1], os.path.join(dir1, frag1)),
            ([dir2, dir1], [frag1], os.path.join(dir2, frag1)),
            ([dir1, dir2, dir3], [frag1], os.path.join(dir1, frag1)),
            ([dir3], [], dir3),
            ([dir1, dir2], [frag2, frag1], os.path.join(dir1, frag2, frag1)),
            ([], [], None)
        ]

        for dirs, paths, expected_output in cases:
            actual_output = multipath.try_join(dirs, *paths)
            self.assertEqual(expected_output, actual_output)

    def test_join_all_returns_list_of_joined_paths(self):
        dir1 = "/some/dir"
        dir2 = "/another/dir"
        dir3 = "a/relative/dir"

        frag1 = "sub1"
        frag2 = "sub2"

        input_dirs = [dir1, dir2, dir3]

        returned_paths = multipath.join_all(input_dirs, frag1, frag2)
        expected_paths = [os.path.join(input_dir, frag1, frag2) for input_dir in input_dirs]
        self.assertEqual(expected_paths, returned_paths)

    def test_join_all_works_for_empty_list(self):
        self.assertEqual([], multipath.join_all([], "ignored", "args"))

    def test_resolve_returns_expected_result_for_nominal_case(self):
        empty_dir = tempfile.mkdtemp()
        dir_containing_file = tempfile.mkdtemp()

        frag1 = "somefile"

        self.__create_empty_file(os.path.join(dir_containing_file, frag1))

        ret = multipath.resolve([empty_dir, dir_containing_file], frag1)

        self.assertEqual(ret, os.path.join(dir_containing_file, frag1))

    def test_resolve_raises_ValueError_if_dirs_is_empty(self):
        with self.assertRaises(ValueError):
            multipath.resolve([], "doesnt", "matter")

    def test_resolve_returns_first_existent_path_even_if_other_paths_have_the_subpath(self):
        empty_dir = tempfile.mkdtemp()
        first_dir_with_file = tempfile.mkdtemp()
        second_dir_with_file = tempfile.mkdtemp()

        path = "somefile"

        self.__create_empty_file(os.path.join(first_dir_with_file, path))
        self.__create_empty_file(os.path.join(second_dir_with_file, path))

        ret = multipath.resolve([empty_dir, first_dir_with_file, second_dir_with_file], path)

        self.assertEqual(ret, os.path.join(first_dir_with_file, path))

    def test_resolve_raises_FileNotFoundError_if_subpath_doesnt_exist_in_any_dir(self):
        empty_dir_1 = tempfile.mkdtemp()
        empty_dir_2 = tempfile.mkdtemp()
        empty_dir_3 = tempfile.mkdtemp()

        path = "some/path"

        with self.assertRaises(FileNotFoundError):
            multipath.resolve([empty_dir_1, empty_dir_2, empty_dir_3], path)

    def test_resolve_return_first_path_in_dirs_when_given_no_subpaths(self):
        empty_dir_1 = tempfile.mkdtemp()
        empty_dir_2 = tempfile.mkdtemp()

        ret = multipath.resolve([empty_dir_1, empty_dir_2])

        self.assertEqual(empty_dir_1, ret)

    def test_resolve_raises_ValueError_if_given_empty_list_of_dirs(self):
        with self.assertRaises(ValueError):
            multipath.resolve([], "some/path")

    def test_try_resolve_returns_expected_result_for_nominal_case(self):
        empty_dir = tempfile.mkdtemp()
        dir_containing_file = tempfile.mkdtemp()

        frag1 = "somefile"

        self.__create_empty_file(os.path.join(dir_containing_file, frag1))

        ret = multipath.try_resolve([empty_dir, dir_containing_file], frag1)

        self.assertEqual(ret, os.path.join(dir_containing_file, frag1))

    def test_try_resolve_returns_first_existent_path_even_if_other_paths_have_the_subpath(self):
        empty_dir = tempfile.mkdtemp()
        first_dir_with_file = tempfile.mkdtemp()
        second_dir_with_file = tempfile.mkdtemp()

        path = "somefile"

        self.__create_empty_file(os.path.join(first_dir_with_file, path))
        self.__create_empty_file(os.path.join(second_dir_with_file, path))

        ret = multipath.try_resolve([empty_dir, first_dir_with_file, second_dir_with_file], path)

        self.assertEqual(ret, os.path.join(first_dir_with_file, path))

    def test_try_resolve_returns_None_if_subpath_doesnt_exist_in_any_dir(self):
        empty_dir_1 = tempfile.mkdtemp()
        empty_dir_2 = tempfile.mkdtemp()
        empty_dir_3 = tempfile.mkdtemp()

        path = "some/path"

        self.assertIsNone(multipath.try_resolve([empty_dir_1, empty_dir_2, empty_dir_3], path))

    def test_try_resolve_return_first_path_in_dirs_when_given_no_subpaths(self):
        empty_dir_1 = tempfile.mkdtemp()
        empty_dir_2 = tempfile.mkdtemp()

        ret = multipath.try_resolve([empty_dir_1, empty_dir_2])

        self.assertEqual(empty_dir_1, ret)

    def test_try_resolve_returns_None_if_given_empty_list_of_dirs(self):
        self.assertIsNone(multipath.try_resolve([], "some/path"))

    def test_resolve_all_returns_expected_result_for_nominal_case(self):
        empty_dir = tempfile.mkdtemp()
        dir_containing_file = tempfile.mkdtemp()

        frag1 = "somefile"

        self.__create_empty_file(os.path.join(dir_containing_file, frag1))

        ret = multipath.resolve_all([empty_dir, dir_containing_file], frag1)

        self.assertEqual(ret, [os.path.join(dir_containing_file, frag1)])

    def test_resolve_all_returns_all_existient_paths(self):
        empty_dir = tempfile.mkdtemp()
        first_dir_with_file = tempfile.mkdtemp()
        second_dir_with_file = tempfile.mkdtemp()

        path = "somefile"

        self.__create_empty_file(os.path.join(first_dir_with_file, path))
        self.__create_empty_file(os.path.join(second_dir_with_file, path))

        ret = multipath.resolve_all([empty_dir, first_dir_with_file, second_dir_with_file], path)

        expected_ret = [
            os.path.join(first_dir_with_file, path),
            os.path.join(second_dir_with_file, path),
        ]

        self.assertEqual(ret, expected_ret)

    def test_resolve_all_returns_empty_list_if_subpath_doesnt_exist_in_any_dir(self):
        empty_dir_1 = tempfile.mkdtemp()
        empty_dir_2 = tempfile.mkdtemp()
        empty_dir_3 = tempfile.mkdtemp()

        path = "some/path"

        ret = multipath.resolve_all([empty_dir_1, empty_dir_2, empty_dir_3], path)

        self.assertEqual([], ret)

    def test_resolve_all_returns_all_paths_in_dirs_when_given_no_subpaths(self):
        empty_dir_1 = tempfile.mkdtemp()
        empty_dir_2 = tempfile.mkdtemp()

        dirs = [empty_dir_1, empty_dir_2]
        ret = multipath.resolve_all(dirs)

        self.assertEqual(ret, dirs)

    def __create_empty_file(self, path):
        open(path, "a").close()
