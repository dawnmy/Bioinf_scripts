#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File: tocami.py --- convert to CAMI profiling format
Created Date: July 17th 2019
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 22nd Nov 2022 4:36:44 pm
'''

import os
import sys
import click
import time
import re
from ete3 import NCBITaxa


@click.command()
@click.option(
    "-f",
    "--format",
    type=click.Choice(["bracken", "motus", "centrifuge",
                       "tipp", "metaphyler", "kraken", "metax"]),
    help="The input profile format",
    required=True)
@click.argument(
    'profile',
    type=click.Path(exists=True),
    required=True)
@click.option(
    '-s',
    '--sampleid',
    type=str,
    required=True,
    help="The sample ID of the input sample. This will present in the header of the output."
)
@click.option(
    '-t',
    '--taxdump',
    type=click.Path(exists=True),
    default=None,
    help="The taxdump.tar.gz file to create database."
)
@click.option(
    '-d',
    '--db',
    type=str,
    help="The folder to store the taxa.sqlite file.",
    required=True)
@click.option(
    '-o', "--output",
    type=str,
    default="",
    help='output CAMI profile file.')
def to_cami(format, profile, sampleid, taxdump, db, output):
    dump_file = taxdump
    dbfile = os.path.join(db, "taxa.sqlite")
    global ncbi
    if os.path.exists(dbfile):
        ncbi = NCBITaxa(dbfile=dbfile)
    else:
        if taxdump is None:
            raise IOError(
                "The db is empty, you must specify the taxdump.tar.gz file to create the database.")
        ncbi = NCBITaxa(dbfile=dbfile, taxdump_file=dump_file)
    header = generate_header(sampleid)
    outstream = (open(output, "w")
                 if output else sys.stdout)
    outstream.write(header)
    if format == "bracken":
        bracken_to_cami(profile, outstream)
    elif format == "kraken":
        kraken_to_cami(profile, outstream)
    elif format == "metax":
        metax_to_cami(profile, outstream)
    elif format == "motus":
        motus_to_cami(profile, outstream)
    elif format == "centrifuge":
        centrifuge_to_cami(profile, outstream)
    elif format == "metaphyler":
        metaphyler_to_cami(profile, outstream)
    elif format == "tipp":
        tipp_to_cami(profile, outstream)

    if output:
        outstream.close()


def bracken_to_cami(profile, outstream):

    # print("Converting {} to CAMI profiling format".format(profile))
    tax_level_dict = {"S": "species",
                      "G": "genus",
                      "F": "family",
                      "O": "order",
                      "C": "class",
                      "P": "phylum",
                      "D": "superkingdom"}
    with open(profile, 'r') as fh:
        for line in fh:
            if not line.startswith("name\ttaxonomy_id"):
                cols = line.strip().split("\t")
                name, taxid, level, rel_abd = [
                    cols[i] for i in [0, 1, 2, 6]]
                level = tax_level_dict[level]
                try:
                    taxon_path = get_taxon_path(taxid)
                except ValueError:
                    continue
                out_cols = [taxid, level, taxon_path[0],
                            taxon_path[1], str(100 * float(rel_abd))]
                outline = "\t".join(out_cols)
                outstream.write(outline + '\n')


def kraken_to_cami(profile, outstream):
    # print("Converting {} to CAMI profiling format".format(profile))
    tax_level_dict = {"S": "species",
                      "G": "genus",
                      "F": "family",
                      "O": "order",
                      "C": "class",
                      "P": "phylum",
                      "D": "superkingdom"}

    tax_level_cami_dict = {"superkingdom": [],
                           "phylum": [],
                           "class": [],
                           "order": [],
                           "family": [],
                           "genus": [],
                           "species": []}

    with open(profile, 'r') as fh:
        for line in fh:
            cols = line.strip().split("\t")
            level, taxid, rel_abd = cols[3], cols[4], cols[0]
            if level not in tax_level_dict or float(rel_abd) == 0:
                continue
            level = tax_level_dict[level]
            try:
                taxon_path = get_taxon_path(taxid)
            except ValueError:
                continue
            out_cols = [taxid, level, taxon_path[0],
                        taxon_path[1], rel_abd]
            tax_level_cami_dict[level].append(out_cols)
            # outline = "\t".join(out_cols)
            # outstream.write(outline + '\n')
    for level, cami in tax_level_cami_dict.items():
        for out_cols in sorted(cami, key=lambda x: float(x[4]),
                               reverse=True):
            outline = "\t".join(out_cols)
            outstream.write(outline + '\n')


def metax_to_cami(profile, outstream):

    # print("Converting {} to CAMI profiling format".format(profile))
    with open(profile, 'r') as fh:
        for line in fh:
            cols = line.strip().split("\t")
            taxid, level, rel_abd = [
                cols[i] for i in [1, 2, 5]]
            # level = 'species'  # tax_level_dict[level]
            if float(rel_abd) > 0:
                try:
                    taxon_path = get_taxon_path(taxid)
                except ValueError:
                    continue
                out_cols = [taxid, level, taxon_path[0],
                            taxon_path[1], rel_abd]
                outline = "\t".join(out_cols)
                outstream.write(outline + '\n')


def motus_to_cami(profile, outstream):
    # print("Converting {} to CAMI profiling format".format(profile))
    with open(profile, 'r') as fh:
        p = re.compile(r" -k (\w+) ")
        for line in fh:
            if line.startswith("# git tag"):
                level = re.findall(p, line)[0]
            elif not line.startswith("#"):
                cols = line.strip().split("\t")
                name, rel_abd = cols
                taxid = get_taxid(name)
                if taxid:
                    taxon_path = get_taxon_path(taxid)
                    out_cols = [taxid, level, taxon_path[0],
                                taxon_path[1], str(100 * float(rel_abd))]
                    outline = "\t".join(out_cols)
                    outstream.write(outline + '\n')
            else:
                continue


def centrifuge_to_cami(profile, outstream):

    tax_level_dict = {"S": "species",
                      "G": "genus",
                      "F": "family",
                      "O": "order",
                      "C": "class",
                      "P": "phylum",
                      "D": "superkingdom"}
    with open(profile, 'r') as fh:
        for line in fh:
            (rel_abd, count, specific_count, level, taxid, name) = [
                col.strip() for col in line.strip().split("\t")]

            if level in tax_level_dict:  # ['U', '-']:
                level = tax_level_dict[level]
                try:
                    taxon_path = get_taxon_path(taxid)
                except ValueError:
                    continue
                out_cols = [taxid, level, taxon_path[0],
                            taxon_path[1], rel_abd]
                outline = "\t".join(out_cols)
                outstream.write(outline + '\n')


def tipp_to_cami(profile, outstream):
    with open(profile, 'r') as fh:
        for line in fh:
            if not (line.startswith("taxa") or line.startswith("unclassified")):
                (taxid, rel_abd) = line.strip().split("\t")
                rel_abd = str(float(rel_abd) * 100)

                try:
                    # name = get_name(taxid)
                    level = get_level(taxid)
                    taxon_path = get_taxon_path(taxid)
                except ValueError:
                    continue
                out_cols = [taxid, level, taxon_path[0],
                            taxon_path[1], rel_abd]

                outline = "\t".join(out_cols)
                outstream.write(outline + '\n')


def metaphyler_to_cami(profile, outstream):
    with open(profile, 'r') as fh:
        for line in fh:
            if not (line.startswith("Name") or line.startswith("Other")):
                (name, rel_abd, _reads) = line.strip().split("\t")

                try:
                    taxid = get_taxid(name)
                    if taxid is None:
                        print(name, "not found")
                        continue

                    level = get_level(taxid)
                    taxon_path = get_taxon_path(taxid)
                except ValueError:

                    continue
                out_cols = [taxid, level, taxon_path[0],
                            taxon_path[1], rel_abd]
                outline = "\t".join(out_cols)
                outstream.write(outline + '\n')


def generate_header(sampleid):
    date = time.strftime("%Y%m%d")

    header = '''# Taxonomic Profiling Output
@SampleID:{}
@Version:0.9.1
@Ranks:superkingdom|phylum|class|order|family|genus|species|strain
@TaxonomyID:ncbi-taxonomy_{}
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE
'''.format(sampleid, date)
    return header


def get_taxid(name):
    taxid = ncbi.get_name_translator([name])
    try:
        return str(taxid[name][0])
    except KeyError:
        return None


def get_name(taxid):
    name = ncbi.get_taxid_translator([taxid])
    try:
        return str(name[taxid][0])
    except KeyError:
        return None


def get_level(taxid):
    taxid = int(taxid)
    level = ncbi.get_rank([taxid])
    try:
        return str(level[taxid])
    except KeyError:
        return None


def get_taxon_path(taxid):
    try:
        taxid_list = ncbi.get_lineage(taxid)
    except ValueError:
        raise
    kept_levels = ["superkingdom", "phylum", "class",
                   "order", "family", "genus", "species", "strain"]

    rank_dict = ncbi.get_rank(taxid_list)
    kept_taxids = []

    for level in kept_levels:
        for k, v in rank_dict.items():
            if v == level:
                kept_taxids.append(k)
    taxsn_dict = ncbi.get_taxid_translator(kept_taxids)
    taxid_path = "|".join(map(str, kept_taxids))
    taxsn_path = "|".join([taxsn_dict[tax] for tax in kept_taxids])
    return [taxid_path, taxsn_path]


if __name__ == "__main__":
    to_cami()
