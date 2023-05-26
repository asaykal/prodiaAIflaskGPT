from setuptools import setup, find_packages

setup(
    name='app',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==2.2.3',
        'requests==2.28.2',
        'openai==0.27.7'
    ],
    entry_points={
        'console_scripts': [
            'app = app:app',
        ],
    },
)
