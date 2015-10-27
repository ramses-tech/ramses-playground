from setuptools import setup, find_packages

requires = ['pyramid']

setup(name='map_my_travels',
      version='0.0.1',
      description='map_my_travels',
      long_description='',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons ramses',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="map_my_travels",
      entry_points="""\
      [paste.app_factory]
          main = map_my_travels:main
      """)
