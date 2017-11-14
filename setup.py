from setuptools import setup

package_name = 'teleop_twist_keyboard'

setup(
    name=package_name,
    version='0.6.0',
    packages=[],
    py_modules=[
        'teleop_twist_keyboard'
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('shared/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    maintainer='Austin Hendrix',
    maintainer_email='namniart@gmail.com',
    author='Graylin Trevor Jay',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: BSD',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='A robot-agnostic teleoperation node to convert keyboard'
                'commands to Twist messages.',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_twist_keyboard = teleop_twist_keyboard:main'
        ],
    },
)
