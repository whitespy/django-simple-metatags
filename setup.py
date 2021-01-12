from setuptools import setup, find_packages


setup(
    name='django-simple-metatags',
    version='2.0.1',
    description="The django application allows to add title, keywords and "
                "description meta tags to site's pages.",
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
    ],
)
