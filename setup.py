from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read().strip()


def version():
    with open('VERSION') as f:
        return f.read().strip()


def requirements():
    with open('requirements.txt') as f:
        return f.read().strip().split('\n')


setup(name='pmserver',
      license='MIT License',
      version=version(),
      author='Mirko Maelicke',
      author_email='mirko.maelicke@kit.edu',
      description='PM10 / PM25 sensor monitoring flask server',
      long_description=readme(),
      install_requires=requirements(),
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False
)
