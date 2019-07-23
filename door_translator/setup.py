from setuptools import find_packages
from setuptools import setup

package_name = 'door_translator'

setup(
    name=package_name,
    version='0.0.1',
    # packages=[],
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    # py_modules=['door_translator'],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Pallavi Gururaj Koty',
    author_email='pallavi.koty@hopetechinik.com',
    maintainer='Pallavi Gururaj Koty',
    maintainer_email='pallavi.koty@hopetechinik.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='door_translator',
    license='Apache License, Version 2.0',
    entry_points={
        'console_scripts': [
            'door_translator = door_translator:main'
        ],
    },
)
