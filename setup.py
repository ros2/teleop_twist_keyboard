from setuptools import setup

setup(
    name='teleop_twist_keyboard',
    version='0.0.0',
    packages=[],
    py_modules=[
        'teleop_twist_keyboard'
    ],
    install_requires=['setuptools'],
    maintainer='Austin Hendrix',
    maintainer_email='namniart@gmail.com',
    author="Graylin Trevor Jay",
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
    entry_points={
        'console_scripts': [
            'teleop_twist_keyboard = teleop_twist_keyboard:main'
        ],
    },
)
