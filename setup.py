from setuptools import setup, find_packages


setup(
    name='django-simple-metatags',
    version='0.9.2',
    description="The django application, that allows attach title, keywords "
                "and description meta tags for site's pages.",
    author='Andrey Butenko',
    author_email='whitespysoftware@gmail.com',
    url='https://github.com/whitespy/django-simple-metatags',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
