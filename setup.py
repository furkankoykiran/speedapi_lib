from setuptools import setup, find_packages

setup(
    name='speedapi_lib',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pydantic',
        'pydantic-settings',
        'bolt11',
    ],
    entry_points={
        'console_scripts': [
            'speedapi_lib=speedapi_lib.main:main',
        ],
    },
    author='Furkan Köykıran',
    author_email='furkankoykiran@gmail.com',
    description='A Python library for interacting with Speed API and managing Lightning Network invoices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/furkankoykiran/speedapi_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
