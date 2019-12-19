from setuptools import setup, find_packages
setup(
    name = 'my_project',
    version = '0.1.0',
    author = 'Raghad Zeidan',
    description = 'advanced system design server-client project',
    packages = find_packages(),
    install_requires = ['click','flask'],
    test_require = ['pytest']
)
