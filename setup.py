from setuptools import setup


setup(
    name="remora",
    version="0.1",
    author="Mitch Garnaat",
    author_email="mitch@garnaat.com",
    description=(
        "A small, annoying parasite stuck to the underside of AWSCLI."
        "It provides a very hacky way of using AWSCLI as a library."
    ),
    keywords="awscli",
    url="https://github.com/garnaat/remora",
    install_requires=['awscli>=1.7.14'],
    py_modules=['remora'],
    classifiers=[
        "Topic :: Utilities",
    ],
)
