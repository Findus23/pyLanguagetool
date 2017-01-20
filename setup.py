from setuptools import setup, find_packages

setup(
    name='pyLanguagetool',
    version='0.0.3',
    packages=find_packages(),
    url='https://github.com/Findus23/pylanguagetool',
    license='MIT',
    author='Lukas Winkler',
    author_email='l.winkler23@mailbox.org',
    description='A python library and CLI for the LanguageTool JSON API',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Environment :: Console",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Text Processing :: Linguistic"
    ],
    install_requires=['colorama', 'configargparse', 'requests'],
    keywords="languagetool spell grammar checker",
    entry_points={
        'console_scripts': [
            'languagetool=pylanguagetool:main',
        ],
    },

)
