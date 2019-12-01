from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='frost-client',
      version='0.1.4',
      description='Python wrapper for the frost.met.no API',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
      ],
      url='https://github.com/BergensTidende/frost-client',
      author='Anders G. Eriksen',
      author_email='anders.eriksen@bt.no',
      license='MIT',
      keywords='weather pandas ',
      packages=find_packages(exclude=('tests',)),
      python_requires='>= 3.6',
      install_requires=[
          'requests'
      ],
      extras_require={
        'pandas':  ["pandas"]
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
