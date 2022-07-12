# Install

To create the environment run:

```
conda env create -f environment.yml --prefix ./env/analog_crossover/
```

and activate using:

```
conda activate ./env/analog_crossover
```

The specific environment (potentially very OS specific) can be exported

```
conda env export --prefix ./env/analog_crossover --file exact_environment.yml
```

and updated:

```
conda env update --prefix ./env/analog_crossover --file exact_environment.yml  --prune
```
