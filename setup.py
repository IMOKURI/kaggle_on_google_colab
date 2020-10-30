from setuptools import setup, find_packages

setup(
    name='kaggle_on_google_colab',
    version='0.0.1',
    url='https://github.com/IMOKURI/kaggle_on_google_colab.git',
    author='IMOKURI',
    author_email='nenegi.01mo@gmail.com',
    description='Setup kaggle environment on Google Colaboratory.',
    packages=find_packages(),
    install_requires=['kaggle'],
)
