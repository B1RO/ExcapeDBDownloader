import requests
import json
import os


print(os.getcwd())
with open('config.json') as f:
    config = json.load(f)

speciesIDDict = {
    "Mouse" : 10090,
    "Rat" :2010116,
    "Human" : 209606
}


def parse_config_to_params(config):
    species_param = "%".join([str(speciesIDDict[x]) for x in config["species"]]) + ")&"
    data_source_param = "DB%3A(" + "%".join([str(x) for x in config["data_sources"]]) + ")&" if len(config["data_sources"]) != 0 else ""
    ortholog_group_param = "Ortholog_Group%3A(" + "%".join("20" + str(config["ortholog_group"])) + ")&" if len(config["ortholog_group"]) != 0 else ""
    gene_symbol_param = "Gene_Symbol%3A(" + "%".join([str(x) for x in config["gene_symbol"]]) + ")&" if len(config["gene_symbol"]) != 0 else ""
    entrez_param = "Entrez_ID%3A(" + "%".join(str(config["entrez_ID"])) + ")&" if len(config["entrez_ID"]) != 0 else ""
    activity_param = "Activity_Flag%3A(" + "%".join("20" + str(config["activity_flag"])) + ")&" if len(config["activity_flag"]) != 0 else ""
    return species_param, data_source_param, ortholog_group_param, gene_symbol_param, entrez_param, activity_param;

species_param, data_source_param, ortholog_group_param, gene_symbol_param, entrez_param, activity_param = parse_config_to_params(config)
print(
    "Using the following parameters:",
    data_source_param,
    ortholog_group_param,
    gene_symbol_param,
    entrez_param,
    activity_param
)

resourceUrl = "https://api.ideaconsult.net/excape/"
res = requests.get(
resourceUrl + 'select?facet=true&facet.field={{!ex=owner_name}}DB&'
'facet.field={{!ex=species}}Tax_ID&'
'facet.field={{!ex=reference}}Ortholog_Group&facet.field={{!ex=protocol}}Gene_Symbol&facet.field={{!ex=entrez}}Entrez_ID&'
'facet.field={{!ex=interpretation}}Activity_Flag&'
'q=*%3A*&facet.limit=-1&facet.mincount=1&'
'f.Entrez_ID.facet.mincount=10&'
'f.Ortholog_Group.facet.mincount=10&'
'fq=%7B!collapse%20field%3Ds_uuid%7D&'
'fq={{!tag=species}}Tax_ID%3A({0})&'
'{1}'
'{2}'
'{3}'
'{4}'
'{5}'
'fl=type_s%3A%22study%22%2Cs_uuid%2Cname%3As_uuid%2Cdoc_uuid%3Aid%2Ctopcategory%3A%22TOX%22%2Cendpointcategory%3ADB%2Cguidance%2CGene_Symbol%2CSMILES%3AGene_Symbol%2Cname%3As_uuid%2Cpublicname%3AOriginal_Entry_ID%2Creference%3AOriginal_Assay_ID%2Creference_owner%3ADB%2Creference_year%3A%222016%22%2Ccontent%3A%22%22%2Cowner_name%3ADB%2CloValue%3ApXC50%2Cowner_name%3A%22ExCAPE%22%2CsubstanceType%3ADB%2CTax_ID%2CEntrez_ID%2Ceffectendpoint%3A%22pXC50%22%2Cinterpretation_result%3AActivity_Flag%2Cunit%3A%22%22&'
'rows=10&'
'json.nl=map&'
'expand=true&'
'expand.rows=20&'
'wt=json'.format(species_param, data_source_param, ortholog_group_param, activity_param, entrez_param, gene_symbol_param)
)

print(res.text)
