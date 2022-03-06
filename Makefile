CONDA = conda

setup:
	$(CONDA) env create --prefix ./.envs/css_proj --file conda.yml

setup_cpu:
	$(CONDA) env create --prefix ./.envs/css_proj --file conda_cpu.yml

setup_pkg_dev:
	python -m pip install -e .
	pre-commit install

setup_pkg:
	python -m pip install .

clean_env:
	$(CONDA) env remove --prefix ./.envs/css_proj

