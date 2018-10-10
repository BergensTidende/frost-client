from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='frost-client',
      version='0.1.2',
      description='Python wrapper for the frost.met.no API',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      url='https://github.com/BergensTidende/frost-client',
      author='Anders G. Eriksen',
      author_email='anders.eriksen@bt.no',
      license='MIT',
      keywords='weather pandas ',
      packages=find_packages(exclude=('tests',)),
      install_requires=[
          'requests',
          'pandas'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
