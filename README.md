## Gene Expression Atlas Base Line Downloader
Downloads the expression values of a given homo sapiens gene list collapsing the information around a specific cell type experiment (*BLUEPRINT common haemopoetic cells*) via the [EBI](https://www.ebi.ac.uk/) API.
#### Usage
```shell
python3 AtlasExpressionBaseLine.py geneList.txt someResults
# 1º the genelist, 2º the name of the output table
less -S someResults.tsv
#   CD14-positive, CD16-negative classical monocyte CD3-positive, CD4-positive, CD8-positive, double positive thymocyte     CD34-, CD41+, CD42+ megakaryocyte cell  CD34-negative, CD41-positive, CD42-posi
# BCL2    3.0     57.0    0.8     2.0     30.0    138.0   138.0   34.0    73.0    8.0     102.0   26.0    23.0    2.0     5.0     21.0    13.0    67.0    34.0    5.0     2.0     2.0     2.0     3.0     0.5
# NR3C1   54.0    70.0    12.0    19.0    30.0    45.0    93.0    26.0    55.0    33.0    42.0    23.0    16.0    49.0    31.0    67.0    46.0    31.0    36q.0    17.0    20.0    46.0    55.0    37.0    65.0
someResults.tsv (END)
```
#### Detail
##### The url-encoded query
Change the line with the url-encoded data query to the API to find the expression values that pass the filters applied, as long as they are available.
```python
# line 57 of the script
# Default data query
"geneQuery=%5B%7B%22value%22%3A%22{}%22%7D%5D&conditionQuery=&species=homo sapiens&source=CELL_TYPE"
# You can change this line to perform other queries with different filters but,
# WARNING if you change this you will probably need to change
# the after download processing (collapse of experiments/rows)
```
This script download and collapse the different experiments into a single vector of gene expression. In our case, we filled the missing data of our key row (below specified) with the following experiments subsequently whenever possible.
```python
# line 36 of the script
# Default row completed with the values of the rest of the experiments
keyrow = 'Cell Types - BLUEPRINT common haemopoetic cells'
```
