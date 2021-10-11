from setuptools import setup

setup(
    name='reddit_app',
    version='0.1.0',
    packages=['reddit_app'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'dash',
        'Flask',
        'html5validator',
        'plotly',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'pytest-mock',
        'requests',
    ],
    python_requires='>=3.6',
)
