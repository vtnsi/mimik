Building the Docs

To build the docs, run the following commands while the Python virtual environment is active:

``` bash
sudo apt-get install pandoc
pip install sphinx sphinx-rtd-theme nbsphinx ipykernel
python -m ipykernel install --user
```