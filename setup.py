from setuptools import setup, find_packages
import carbon_tracker

NAME = 'carbon-tracker'
VERSION = '0.1.0'


def setup_package():
    metadata = dict(name=NAME,
                    version=VERSION,
                    packages=find_packages(),
                    package_data={'': ['*.csv']},
                    include_package_data=True)

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
