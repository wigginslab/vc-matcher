from setuptools import setup, find_packages

setup(
    name='vc-matcher',
    version='0.1.0',
    install_requires=[
        'flask==0.9',
        'flask-sqlalchemy',
        'psycopg2',
        'gunicorn',
        'numpy',
        'nltk',
        'scikit-learn',
        'scipy'
    ],
    url='http://github.com/wigginslab/vc-matcher',
    description=("VC predictions"),
    packages=find_packages(),
)