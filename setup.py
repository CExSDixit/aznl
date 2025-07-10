from setuptools import setup

setup(
    name='aznl',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'openai',
        'requests',
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        aznl=main:main
    ''',
    author='Your Name',
    description='Natural language Azure CLI query tool using LLMs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 