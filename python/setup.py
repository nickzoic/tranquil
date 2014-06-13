from distutils.core import setup

setup(
    name="tranquil",
    version="0.0.1",
    author="Nick Moore",
    author_email="nick@zoic.org",
    url="https://github.com/nickzoic/tranquil",
    description="Tranquil Python Implementation",
    download_url="http://github.com/nickzoic/tranquil/tarball/0.0.1",
    keywords=["json", "ajax"],
    license='BSD',
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    py_modules=['tranquil'],
)
