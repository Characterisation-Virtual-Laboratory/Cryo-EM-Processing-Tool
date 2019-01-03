#!/bin/bash

#Setup Jupyter Notebook
echo '** Installing Jupyter **'
python3 -m pip install --upgrade pip
python3 -m pip install jupyter

echo '** Installing Python Libraries **'
pip3 install mrcfile
pip3 install Pillow
pip3 install pandas
pip3 install ipympl

#Setup Jupyter Lab
echo '** Installing Jupyter Lab**'
pip3 install jupyterlab

#Setup Jupyter Widgets for both Notebook and lab. Lab requires Node.
#node --version to check the details. jupyter lab required version >= 6.11.5
echo '** Install Widgets **'
pip3 install ipywidgets
echo '** Enable Widgets for Jupyter Notebook and Lab  **'
jupyter nbextension enable --py widgetsnbextension

#Installing Widgets to Jupyter Lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager

#Install matplotlib to Jupyter Lab
jupyter labextension install jupyter-matplotlib
