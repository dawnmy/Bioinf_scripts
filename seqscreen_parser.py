#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rich_click as click
import pandas as pd

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=str)
def parse_seqscreen(input, output):
    """Parse SeqScreen output file to a tabular format."""
    
    df = pd.read_csv(input, sep='\t', index_col=0, na_values='-')
    pathogenicity_features = df.loc[:, 'disable_organ':'virulence_regulator'].fillna(0).astype(int).sum(axis=1)

    pathogenic_genes_df = df.loc[pathogenicity_features > 0, ['taxid', 
                                                              'centrifuge_multi_tax', 
                                                              'diamond_multi_tax',
                                                              'go',
                                                              'multi_taxids_confidence',
                                                              'go_id_confidence',
                                                              'size',
                                                            'organism',
                                                            'gene_name',
                                                            'uniprot',
                                                            'uniprot evalue']]
    
    pathogenic_genes_df['taxid'] = pathogenic_genes_df['taxid'].astype(int)
    
    pathogenic_genes_df.index.name = 'gene'
    
    
    pathogenic_genes = pathogenicity_features[pathogenicity_features > 0].index
    
    gene_pathogenicity_features_dict = {}
    
    for gene, row in df.loc[pathogenic_genes,'disable_organ':'virulence_regulator'].iterrows():
        gene_pathogenicity_features_dict[gene] = ';'.join(row[row>0].index)
    
    pathogenicity_df = pd.DataFrame.from_dict(gene_pathogenicity_features_dict, 
                                 orient='index',
                                 columns=['Pathogenicity'])

    pathogenicity_df.index.name = 'gene'

    pd.merge(pathogenic_genes_df, pathogenicity_df, left_index=True, right_index=True).to_csv(output, sep='\t')

parse_seqscreen()
