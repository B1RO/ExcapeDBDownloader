import json

import matplotlib
import pandas as pd
import requests
import seaborn as sns;
import matplotlib.pyplot as plt;


def query_target_counts():
    res = requests.get(
        'https://api.ideaconsult.net/excape/select?facet=true&facet.field={!ex=owner_name}DB&facet.field={'
        '!ex=species}Tax_ID&facet.field={!ex=reference}Ortholog_Group&facet.field={'
        '!ex=protocol}Gene_Symbol&facet.field={!ex=entrez}Entrez_ID&facet.field={'
        '!ex=interpretation}Activity_Flag&q=*%3A*&facet.limit=-1&facet.mincount=1&f.Entrez_ID.facet.mincount=10&f'
        '.Ortholog_Group.facet.mincount=10&fq=%7B!collapse%20field%3Ds_uuid%7D&fl=type_s%3A%22study%22%2Cs_uuid'
        '%2Cname%3As_uuid%2Cdoc_uuid%3Aid%2Ctopcategory%3A%22TOX%22%2Cendpointcategory%3ADB%2Cguidance%3AGene_Symbol'
        '%2Cname%3As_uuid%2Cpublicname%3AOriginal_Entry_ID%2Creference%3AOriginal_Assay_ID%2Creference_owner%3ADB'
        '%2Creference_year%3A%222016%22%2Ccontent%3A%22%22%2Cowner_name%3ADB%2CloValue%3ApXC50%2Cowner_name%3A'
        '%22ExCAPE%22%2CsubstanceType%3ADB%2CTax_ID%2CEntrez_ID%2Ceffectendpoint%3A%22pXC50%22'
        '%2Cinterpretation_result%3AActivity_Flag%2Cunit%3A%22%22&rows=10&json.nl=map&expand=true&expand.rows=20&wt'
        '=json')
    return res.json()["facet_counts"]["facet_fields"]

gene_target_counts = query_target_counts()['Gene_Symbol']
plt.rcParams.update({'font.size': 8})
df = pd.DataFrame(gene_target_counts.items(), columns=['Gene', 'Count'])
plt.xticks(rotation=45);
ax = sns.barplot(x="Gene", y="Count", data=df.sort_values('Count',ascending=False).head(15))
plt.savefig('target_counts.png')
