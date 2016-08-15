from setuptools import setup

setup(
    name='PokemonVortexV3Catcher',
    version='0.1.0',
    author='Kyzaghan',
    author_email='ik@ismailkose.com.tr',
    scripts=['run.py'],
    description='Pokemon Vortex V3 AUTO CATCHER',
    install_requires=[
    "beautifulsoup4 >= 4",
    "requests >= 2",
    "colorama >= 0.3",
],
)