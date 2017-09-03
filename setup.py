from setuptools import setup
import os

requirements = os.path.join(os.path.dirname(__file__), 'requirements.txt')

setup(
    name='img_processor',
    version='0.1',
    description='Image processing microservice',
    url='https://github.com/justinbarrick/img_processor',
    packages=['img_processor'],
    install_requires=[ r.rstrip() for r in open(requirements).readlines() ]
)
