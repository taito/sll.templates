from setuptools import find_packages
from setuptools import setup


setup(
    name='sll.templates',
    version='1.11.4',
    description="Templates for SLL site.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@abita.fi',
    url='https://github.com/taito/sll.templates',
    license='None-free',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['sll'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.PloneFormGen',
        'collective.base',
        'collective.contentleadimage',
        'collective.cropimage',
        'hexagonit.socialbutton',
        'setuptools',
        'sll.basetheme'],
    extras_require={'test': ['Products.CMFPlacefulWorkflow', 'hexagonit.testing']},
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
