---
title: Manual Installation, Windows
---

# :fontawesome-brands-windows: Windows

## **Notebook install (semi-automated)**

We have a
[Jupyter notebook](https://github.com/invoke-ai/InvokeAI/blob/main/notebooks/Stable-Diffusion-local-Windows.ipynb)
with cell-by-cell installation steps. It will download the code in this repo as
one of the steps, so instead of cloning this repo, simply download the notebook
from the link above and load it up in VSCode (with the appropriate extensions
installed)/Jupyter/JupyterLab and start running the cells one-by-one.

Note that you will need NVIDIA drivers, Python 3.10, and Git installed
beforehand - simplified
[step-by-step instructions](https://github.com/invoke-ai/InvokeAI/wiki/Easy-peasy-Windows-install)
are available in the wiki (you'll only need steps 1, 2, & 3 ).

## **Manual Install**

### **pip**

See
[Easy-peasy Windows install](https://github.com/invoke-ai/InvokeAI/wiki/Easy-peasy-Windows-install)
in the wiki

---

### **Conda**

1. Install Anaconda3 (miniconda3 version) from [here](https://docs.anaconda.com/anaconda/install/windows/)

2. Install Git from [here](https://git-scm.com/download/win)

3. Launch Anaconda from the Windows Start menu. This will bring up a command
   window. Type all the remaining commands in this window.

4. Run the command:

    ```batch
    git clone https://github.com/invoke-ai/InvokeAI.git
    ```

    This will create stable-diffusion folder where you will follow the rest of
    the steps.

5. Enter the newly-created InvokeAI folder. From this step forward make sure that you are working in the InvokeAI directory!

    ```batch
    cd InvokeAI
    ```

6. Run the following two commands:

    ```batch title="step 6a"
    conda env create
    ```

    ```batch title="step 6b"
    conda activate invokeai
    ```

    This will install all python requirements and activate the "invokeai" environment
    which sets PATH and other environment variables properly.

    Note that the long form of the first command is `conda env create -f environment.yml`. If the
    environment file isn't specified, conda will default to `environment.yml`. You will need
    to provide the `-f` option if you wish to load a different environment file at any point.

7. Load the big stable diffusion weights files and a couple of smaller machine-learning models:

    ```bash
    (invokeai) ~/InvokeAI$ python3 scripts/preload_models.py
    ```

    !!! note
    	This script will lead you through the process of creating an account on Hugging Face,
	accepting the terms and conditions of the Stable Diffusion model license, and
	obtaining an access token for downloading. It will then download and install the
	weights files for you.

	Please see [../features/INSTALLING_MODELS.md] for a manual process for doing the
	same thing.

8. Start generating images!

    # Command-line interface
    (invokeai) python scripts/invoke.py

    # or run the web interface on localhost:9090!
    (invokeai) python scripts/invoke.py --web

    # or run the web interface on your machine's network interface!
    (invokeai) python scripts/invoke.py --web --host 0.0.0.0

To use an alternative model you may invoke the `!switch` command in
the CLI, or pass `--model <model_name>` during `invoke.py` launch for
either the CLI or the Web UI. See [Command Line
Client](../features/CLI.md#model-selection-and-importation). The
model names are defined in `configs/models.yaml`.

9. Subsequently, to relaunch the script, first activate the Anaconda
command window (step 3),enter the InvokeAI directory (step 5, `cd
\path\to\InvokeAI`), run `conda activate invokeai` (step 6b), and then
launch the invoke script (step 9).

!!! tip "Tildebyte has written an alternative"

    ["Easy peasy Windows install"](https://github.com/invoke-ai/InvokeAI/wiki/Easy-peasy-Windows-install)
    which uses the Windows Powershell and pew. If you are having trouble with
    Anaconda on Windows, give this a try (or try it first!)

---

This distribution is changing rapidly. If you used the `git clone` method
(step 5) to download the stable-diffusion directory, then to update to the
latest and greatest version, launch the Anaconda window, enter
`stable-diffusion`, and type:

```bash
git pull
conda env update
```

This will bring your local copy into sync with the remote one.
