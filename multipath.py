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
"""
This module implements functions for working with multiple directories at once.

A common use-case is when a project needs to build paths relative to multiple root directories and return the first path
that exists. This module supplies the `resolve` method for doing that.
"""
import os


def join(dirs, *paths):
    """
    Returns the first dir in `dirs` joined with `*paths` using `os.path.join`.

    :param dirs: A list of dir strings
    :param paths: Path components to join onto the first dir in `dirs`
    :return: A path created by calling `os.path.join` on the first dir in `dirs` with `*paths`.
    :raises: ValueError: if `dirs` is empty
    """
    ret = try_join(dirs, *paths)
    if ret is None:
        raise ValueError("dirs empty: cannot join paths onto nothing: dirs must contain at least one element")
    else:
        return ret


def try_join(dirs, *paths):
    """
    Returns the first dir in `dirs` joined with `*paths` using `os.path.join`, or None if `dirs` is empty.

    :param dirs: A list of dir strings
    :param paths: Path components to join onto the first dir in `dirs`
    :return: A path created by calling `os.path.join` on the first dir in `dirs` with `*paths`, or None if `dirs` is
    empty.
    """
    if len(dirs) == 0:
        return None
    else:
        return os.path.join(dirs[0], *paths)


def join_all(dirs, *paths):
    """
    Returns a list of paths created by calling `os.path.join` on each dir in `dirs` with `*paths`.

    :param dirs: A list of dir strings
    :param path: Path components to join onto each dir in `dirs`
    :return: A list of paths created by calling `os.path.join` on each dir in `dirs` with `*paths`
    """
    return [os.path.join(d, *paths) for d in dirs]


def resolve(dirs, *paths):
    """
    Joins `paths` onto each dir in `dirs` using `os.path.join` until one of the join results is found to exist and
    returns the existent result.

    :param dirs: A list of dir strings to resolve against
    :param paths: Path components to join onto each dir in `dirs`
    :return A path created by calling `os.path.join` on a dir in `dirs` with `*paths`.
    :raises ValueError: If `dirs` is empty
    :raises FileNotFoundError: If joining `paths` onto all dirs in `dirs` always resulted in non-existent paths.
    """
    if len(dirs) == 0:
        raise ValueError("dirs empty: cannot resolve paths against *no* dirs: dirs must contain at least one element")

    ret = try_resolve(dirs, *paths)

    if ret is not None:
        return ret
    elif len(dirs) == 1:
        raise FileNotFoundError("{path}: No such file or directory".format(path=os.path.join(dirs[0], *paths)))
    else:
        attempted_paths = [os.path.join(d, *paths) for d in dirs]
        path = os.path.join(*paths)
        attempt_str = ", ".join(list(map(lambda p: "'" + p + "'", attempted_paths)))
        raise FileNotFoundError("{path}: could not be found after trying {paths}".format(path=path, paths=attempt_str))


def try_resolve(dirs, *paths):
    """
    Joins `paths` onto each dir in `dirs` using `os.path.join` until one of the join results is found to exist and
    returns the existent result. If none of the results exist, returns None.

    :param dirs: A list of dir strings to resolve against
    :param paths: Path components to join onto each dir in `dirs`
    :return A path created by calling `os.path.join` on a dir in `dirs` with `*paths`, or None if joining `paths` onto
    all dirs in `dirs` always resulted in a non-existent path
    """
    for d in dirs:
        path = os.path.join(d, *paths)
        if os.path.exists(path):
            return path
    return None


def resolve_all(dirs, *paths):
    """
    Returns a list of paths created by joining `paths` onto each dir in `dirs` using `os.path.join` and discarding all
    join results that do not exist.

    :param dirs: A list of dir strings to resolve against
    :param paths: Path components to join onto each dir in `dirs` with `os.path.join`
    :return: A list of paths created by joining `paths` onto each dir in `dirs` using `os.path.join` and discarding all
    join results that do not exist.
    """
    return [d for d in join_all(dirs, *paths) if os.path.exists(d)]
