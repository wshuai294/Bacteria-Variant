# Identify variants by mapping reads onto the reference

## Install

- use the conda environment by 
```
conda env create --prefix=edit -f environment.yml
conda activate edit
```
- or install these tools and add them to system path
```
samtools
bwa
freebayes
svaba
```

## Test
```
cd test/
sh test.sh
```

## Run
```
python map_variant.py -h
```
