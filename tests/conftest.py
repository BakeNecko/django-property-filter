
import pytest

from tests.common import is_travis_build


def pytest_collection_modifyitems(items):
    for item in items:
        skip_travis = item.get_closest_marker('skiptravis')

        # Don't count in coverage even when running to not be surprised later
        if skip_travis:
            item.add_marker(pytest.mark.no_cover)

            # Skip if run on Travis
            if is_travis_build():
                print(F'Skip {item} because is Travis Build')
                item.add_marker(pytest.mark.skip)
