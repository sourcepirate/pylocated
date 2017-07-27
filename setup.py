from setuptools import setup

def readme():
    return open("README.md", "r").read()

requirements = []

setup(
    name = 'pylocated',
    packages = ['pylocated'],
    version = '2.0.1',
    long_description= readme(),
    description = "python interface for locate command",
    author='plasmashadow',
    author_email='plasmashadowx@gmail.com',
    url='https://github.com/plasmashadow/pylocated.git',
    license="MIT",
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
    install_requires= requirements,
    test_suite='tests'
)
