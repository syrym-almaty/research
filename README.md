# Research

---

## install conda and run your env

```bash
conda init bash
conda create --name research_1 python=3.11
conda activate research_1
conda deactivate
pip install -r requirements.txt
conda install tensorflow librosa matplotlib pandas seaborn scikit-learn
python --version
conda remove --name research_1 --all
conda env list
conda update --all
python -m pip install --upgrade pip
#--strict-channel-priority: This ensures that Conda considers compatibility of all packages when performing the update. It won’t update to the latest versions unless they are fully compatible with the rest of the environment.
conda update --all --strict-channel-priority
conda update --all --strict-channel-priority python=3.11



```

---

## run your venv

```bash
mkdir ~/venvs
python -m venv ~/venvs/research_1
source ~/venvs/research_1/Scripts/activate
deactivate
```

---

## install dependencies

```python

pip install -r requirements.txt

```

---
