from setuptools import setup

VERSION = '0.1'

setup(
    install_requires=['redis', 'aioredis'],
    name='redisconfig',
    version=VERSION,
    py_modules=['redisconfig'],
    url='https://github.com/sashgorokhov/redisconfig',
    download_url='https://github.com/sashgorokhov/redisconfig/archive/master.zip',
    keywords=['redis', 'configuration'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    long_description='',
    license='MIT License',
    author='sashgorokhov',
    author_email='sashgorokhov@gmail.com',
    description='redisconfig',
)
