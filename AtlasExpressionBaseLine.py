#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
# __author__ = "Adrian Garcia-Moreno"
# __copyright__ = "GENyO BioInformatics Unit 2019"
# __license__ = "GPL"
# __version__ = "0.0.1"
# __email__ = "bioinfo@genyo.es"
# __status__ = "Production"
########################################

def getExprs(atlasexp):
    expressions = [row['expressions'] for row in atlasexp['profiles']['rows']]
    AllExprs = []
    for expression in expressions:
        myexpressions = []
        for values in expression:
            if bool(values):
                value = values['value']
            else:
                value = numpy.nan #None
            myexpressions.append(value)
        AllExprs.append(myexpressions)
    return(AllExprs)

def getATLASexprTable(atlasexp):
    columns = [column['assayGroupId'] for column in atlasexp['columnHeaders']]
    names = [row['name'] for row in atlasexp['profiles']['rows']]
    myexpressions = getExprs(atlasexp)
    exprDF = pandas.DataFrame(index=names, columns=columns)
    for nameIDX in range(0,len(names)):
        exprDF.loc[names[nameIDX],:] = myexpressions[nameIDX]
    return(exprDF)

def fillKeyRow(exprDF):
    keyrow = 'Cell Types - BLUEPRINT common haemopoetic cells'
    rows = exprDF.index.values.tolist()
    if keyrow not in rows:
        keyrow = rows[0]
        print("NO expected row")
        print("\n".join(rows))
    else:
        print("expected row")
        print(keyrow)
    rows.remove(keyrow)
    nulls = exprDF.loc[keyrow,].isnull()
    for row in rows:
        exprDF.loc[keyrow,nulls] = exprDF.loc[row,nulls]
        nulls = exprDF.loc[keyrow,].isnull()
        if numpy.all(nulls):
            return(exprDF.loc[keyrow,])
    return(exprDF.loc[keyrow,])

def getAtlasBaseLineExpr(geneList, tableName="atlasBaseExpr", outdir="."):
    url = 'https://www.ebi.ac.uk/gxa/json/baseline_experiments'
    headers = {"accept":"application/json","accept-language":"en,en-US;q=0.9,es;q=0.8","cache-control":"no-cache","content-type":"application/x-www-form-urlencoded","pragma":"no-cache"}
    thedata = "geneQuery=%5B%7B%22value%22%3A%22{}%22%7D%5D&conditionQuery=&species=homo sapiens&source=CELL_TYPE"
    exprDFs = pandas.DataFrame()
    NOinfoGenes = []
    for gene in geneList:
        print(gene)
        atlasexpreresp = requests.post(url, headers=headers, data=thedata.format(gene))
        atlasexp = json.loads(atlasexpreresp.text)
        if 'error' in atlasexp:
            print('No Info')
            NOinfoGenes.append(gene)
            continue
        exprDF = getATLASexprTable(atlasexp)
        exprDF = fillKeyRow(exprDF)
        exprDF.name = gene
        exprDFs = exprDFs.append(exprDF)
    output = path.join(outdir,tableName+".tsv")
    exprDFs.to_csv(output,sep="\t")
    print("WARNING (genes without info):\n{}".format(",".join(NOinfoGenes)))
    return(exprDFs)

import json, requests, pandas, numpy,  sys
from os import path

geneList_file = sys.argv[1]
tableName = sys.argv[2]

geneList = open(geneList_file,"r").read().splitlines()
getAtlasBaseLineExpr(geneList, tableName, outdir=".")
