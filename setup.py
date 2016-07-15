from setuptools import setup, find_packages
import os

version = '0.4'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n')

setup(name='medialog.lxml',
      version=version,
      description="A Product to embed/add/migrate content with lxml",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='embed plone lxml migrate csv impoort',
      author='Espen Moe-Nilssen',
      author_email='espen@medialog.no',
      url='http://github.com/espenmn/medialog.lxml',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['medialog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.z3cform.datagridfield',
          'cssselect',
          'medialog.controlpanel',
          'plone.api',
          'plone.directives.form',
          'requests',
          'plone.behavior'

          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
