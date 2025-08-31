# spinal-population-dynamics-paper
Code to reproduce the figures from Wimalasena et al. 2025

## 🛠️ Environment Setup

To ensure reproducibility, this repository includes an `environment.yml` file specifying the required Python packages and versions.

### 🔧 Create the Conda Environment

Make sure you have [conda](https://docs.conda.io/en/latest/miniconda.html) or [mamba](https://mamba.readthedocs.io/) installed.

Then run:

```bash
conda env create -f environment.yml
```

This will create a new conda environment (named `spinal-pop-dyn-figs` or as specified in the YAML file).

### ▶️ Activate the Environment

Once created, activate the environment:

```bash
conda activate spinal-pop-dyn-figs
```

You are now ready to run the figure generation scripts.

---

## 🧪 Generating Figures

### 🚀 Suggested Method (VSCode Interactive Window)

The recommended way to run the figure scripts is to open them in **Visual Studio Code** and use the **Interactive Python window** (e.g., Jupyter-style cells). This allows step-by-step execution and interactive debugging.

Each script is designed to generate one figure directly from the source data in `data/SourceData.xlsx`.

> ⚠️ Make sure the data file is present before running scripts. See `data/README.md` for setup instructions.

### 👥 Switching Between Subjects

Some figure scripts support switching between subjects via a `C_ID` variable defined near the top of the file.

To generate figures for a specific subject:

```python
C_ID = "1"  # or "2"
```