def create_request_url(config, start, n_rows):
    species_param, data_source_param, ortholog_group_param, gene_symbol_param, entrez_param, activity_param = parse_config_to_params(
        config)
    return 'https://api.ideaconsult.net/excape/' \
           'select?facet=true&facet.field={{!ex=owner_name}}DB&' \
           'facet.field={{!ex=species}}Tax_ID&' \
           'facet.field={{!ex=reference}}Ortholog_Group&facet.field={{!ex=protocol}}Gene_Symbol&facet.field={{!ex=entrez}}Entrez_ID&' \
           'facet.field={{!ex=interpretation}}Activity_Flag&' \
           'q=*%3A*&facet.limit=-1&facet.mincount=1&' \
           'f.Entrez_ID.facet.mincount=10&' \
           'f.Ortholog_Group.facet.mincount=10&' \
           'fq=%7B!collapse%20field%3Ds_uuid%7D&' \
           'fq={{!tag=species}}' \
           '{0}' \
           '{1}' \
           '{2}' \
           '{3}' \
           '{4}' \
           '{5}' \
            'fl = Ambit_InchiKey%3' \
            'As_uuid%2' \
            'COriginal_Entry_ID%2' \
            'CEntrez_ID%2' \
            'CActivity_Flag%2' \
            'CpXC50%2' \
            'CDB%2' \
            'COriginal_Assay_ID%2' \
            'CTax_ID%2' \
            'CGene_Symbol%2' \
            'COrtholog_Group%2' \
            'CSMILES&' \
           'rows={6}&' \
           'start={7}&' \
           'json.nl=map&' \
           'expand=true&' \
           'expand.rows=20&' \
           'wt=json'.format(species_param, data_source_param, ortholog_group_param, activity_param, entrez_param,
                            gene_symbol_param, n_rows, start)


def parse_config_to_params(config):
    species_id_dict = {
        "Mouse": 10090,
        "Rat": 2010116,
        "Human": 209606
    }
    species_param = "Tax_ID%3A(" + "%".join([str(species_id_dict[x]) for x in config["species"]]) + ")&"if len(
        config["species"]) != 0 else ""
    data_source_param = "DB%3A(" + "%".join([str(x) for x in config["data_sources"]]) + ")&" if len(
        config["data_sources"]) != 0 else ""
    ortholog_group_param = "Ortholog_Group%3A(" + "%20".join(str(config["ortholog_group"])) + ")&" if len(
        config["ortholog_group"]) != 0 else ""
    gene_symbol_param = "Gene_Symbol%3A(" + "%20".join([str(x) for x in config["gene_symbol"]]) + ")&" if len(
        config["gene_symbol"]) != 0 else ""
    entrez_param = "Entrez_ID%3A(" + "%20".join(str(config["entrez_ID"])) + ")&" if len(config["entrez_ID"]) != 0 else ""
    activity_param = "Activity_Flag%3A(" + "%20".join(str(config["activity_flag"])) + ")&" if len(
        config["activity_flag"]) != 0 else ""
    return species_param, data_source_param, ortholog_group_param, gene_symbol_param, entrez_param, activity_param;
