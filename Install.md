## Installing the Cryo-EM Processing Tool

The Cryo-EM Processing Tool runs as a JupyterLab Notebook on the CVL@M3 Desktop.

If you have already installed the Cryo-EM Processing Tool go to the [User guide for the Cryo-EM Processing Tool](./userGuide.md) page for information on using the tool.

Start your CVL@M3 Desktop. An 'Advanced' Desktop is recommended to gain suitable GPU performance.  
For further information on accessing and using a CVL Desktop go to the CVL website's [Getting started on the CVL@M3 Desktop](https://www.cvl.org.au/cvl-desktop/getting-started-with-the-cvl) page.

1. Clone the GitHub repository.

    ```
    git clone https://github.com/Characterisation-Virtual-Laboratory/Cryo-EM-Processing-Tool.git
    ```

2. Setup a python3 virtual environment.

   ```
   /usr/local/python/3.6.2-static/bin/python3 -m venv Cryo-EM-Processing-Tool
   ```

3. Activate the virtual environment.

  ```
  source Cryo-EM-Processing-Tool/bin/activate
  ```

4. Install JupyterLab, widgets and required Python libraries.

  ```
  cd Cryo-EM-Processing-Tool
  bash installNotebook.sh
  ```

5. Load required HPC modules.

  ```
  module load motioncor2/2.1
  module load gctf/1.06_cuda8
  module load gautomatch/0.56
  ```

6. Start JupyterLab. This will cause your web browser to open and display JupyterLab. If you are not familiar with JupyterLab, please refer to the [documentation.](https://jupyterlab.readthedocs.io/en/stable/)

  ```
  jupyter lab
  ```

Once you have installed JupyterLab go to the [User guide for the Cryo-EM Processing Tool]() page for information on using the Cryo-EM Processing Tool.
