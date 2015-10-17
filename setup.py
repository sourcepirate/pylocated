from setuptools import setup

def readme():
    return open("README.md", "r").read()

requirements = [
    'six'
]

setup(
    name = 'pylocated',
    packages = ['pylocated'],
    version = '1.0.0',
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
    install_requires= requirements
)