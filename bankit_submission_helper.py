# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# read file and create annotation table

# %%

import pandas as pd
annotation = pd.read_excel(r'E:\Work\Python\для Паши\VEsP-2 rast annotation.xls') #_.xls file input 
annotation_contents = pd.DataFrame(annotation, columns = ['contig_id', 'feature_id', 'type', 'location', 'start', 'stop', 'strand', 'function',
                                                            'aliases', 'figfam', 'evidence_codes', 'nucleotide_sequence', 'aa_sequence'])

# %% [markdown]
# create lists with interesting features from the columns of the original table (annotation_contents)

# %%
start = annotation_contents.iloc[:, 4].tolist()
stops = annotation_contents.iloc[:, 5].tolist()
functions = annotation_contents.iloc[:, 7].tolist()
types = annotation_contents.iloc[:, 2].tolist()

# %% [markdown]
# To describe our object, the values transl_table = 11 and codon_start 1 are used. Here the script creates creates lists with the specified features values in expected format.

# %%

transl_table = []
size = len(start)
transl_table.append('\n'+'\t'*3+'transl_table'+'\t'+'11')
transl_table = transl_table*size

codon_start = []
codon_start.append ('\n'+'\t'*3+'codon_start'+'\t'+'1')
codon_start = codon_start*size

# %% [markdown]
# create a list with types according to the required format (tabulation)

# %%
new_types = []
for i in types:
    if i=='peg':
        new_types.append('\t' + 'CDS')
    if i=='repeat':
        new_types.append('\t' +'repeat_region')
    if i=='rna':
        for j in functions:
            if 'tRNA' in j:
               new_types.append('\t' +'tRNA') 
               break
            if 'mRNA'in j:
                new_types.append('\t' +'mRNA') 

# %% [markdown]
# find indexes for RNA

# %%
index_new_types_trna = []
l=0
for i in new_types:
    l+=1
    if i == ('\t' +'tRNA') or i==('\t' +'mRNA') :
        index_new_types_trna.append(l)
           

# %% [markdown]
# Removes transl_table and codon_start features for RNA

# %%
for i in index_new_types_trna:
    for j in range(len(transl_table)):
        if i==j:
            transl_table[j-1] = ''
            codon_start[j-1] = ''
            

# %% [markdown]
# search index of repeat_region

# %%
index_repeat_region = []
l=0
for i in new_types:
    l+=1
    if i == ('\t' +'repeat_region') or i==('\t' +'repeat') :
        index_repeat_region.append(l)

# %% [markdown]
# Finds matching indices in the list function and index_repeat_region. Instert rpt_type when indexes match

# %%
for i in index_repeat_region:
    for j in range(len(function)+1):
        #print(i)
        if i==j:
            transl_table[j-1] = ''
            transl_table[j-1] =  ('\n'+'\t'*3 +'rpt_type' + '\t')+ input("Insert one: tandem, inverted, flanking, terminal, direct, dispersed, and other")
            codon_start[j-1] = ''
            function [j-1] = ''

# %% [markdown]
# Adding tabs, new paragraphs for requirements.

# %%
stop =  ['\t' + str(stop) for stop in stops] 
function=  ['\n'+'\t'*3+'product ' + str(function) for function in functions] 

# %% [markdown]
# Packing lists into a single list

# %%
#sorting
n = [list(item) for item in zip(start, stop,new_types, function,transl_table, codon_start)]

# %% [markdown]
# Export the resulting list to txt

# %%

import csv
with open('test.txt', 'w') as f:
    writer = csv.writer(f, lineterminator = '\r', quoting=csv.QUOTE_NONE, quotechar=',',escapechar='\\')
    writer.writerows(n)

# %% [markdown]
# Many unnecessary characters appear when saving. To remove them, txt is imported, unnecessary characters are removed and the list is saved in txt

# %%
#table output

s=[]
file = open('test.txt')
for line in file:
    line = line.rstrip(',')

    for i in line:
        if ',' in line:
            line=line.replace(',', '')
        if  "\\" in line:
            line=line.replace('\\', '')
    line = line.replace('\\', '',1)
    s.append(str(line))

with open('test2.txt', 'w') as f:
    f.writelines(s)
    
#print(*s)


