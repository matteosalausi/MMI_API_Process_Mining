#Import csv file

import pandas as pd
import numpy as np

# Load the data

data = pd.read_csv('/Users/matteosala/Desktop/Master Management and Informatics/Sem4/Thesis/Dataset/Detailed_version.csv')

# Check data

print(data.head())

# Drop useless columns

data = data.drop('Unnamed: 0', axis=1)

# Extract unique values from breaking_change_ids column

unique_values_bc = data['breaking_changes_ids'].apply(lambda x: pd.Series(x.strip('[]').split(','))).stack().unique().tolist()
unique_values_nbc = data['non_breaking_changes_ids'].apply(lambda x: pd.Series(x.strip('[]').split(','))).stack().unique().tolist()
unique_values_unknown = data['unknown_changes_ids'].apply(lambda x: pd.Series(x.strip('[]').split(','))).stack().unique().tolist()

# Mapping the values to a set of categories

breaking_change_mapping = {}
non_breaking_change_mapping = {}
unknown_change_mapping = {}

for item in unique_values_bc:
    if ('api' or 'endpoint') in item.lower():
        breaking_change_mapping[eval(item.strip())] = 'API change'
    if 'response' in item.lower():
        breaking_change_mapping[eval(item.strip())] = 'Response change'
    if 'request' in item.lower():
        breaking_change_mapping[eval(item.strip())] = 'Request change'

for item in unique_values_nbc:
    if 'api' in item.lower():
        non_breaking_change_mapping[eval(item.strip())] = 'API change'
    if 'endpoint' in item.lower():
        non_breaking_change_mapping[eval(item.strip())] = 'API change'
    if 'response' in item.lower():
        non_breaking_change_mapping[eval(item.strip())] = 'Response change'
    if 'request' in item.lower():
        non_breaking_change_mapping[eval(item.strip())] = 'Request change'

for item in unique_values_unknown:
    if ('api' or 'endpoint') in item.lower():
        unknown_change_mapping[eval(item.strip())] = 'API change'
    if 'response' in item.lower():
        unknown_change_mapping[eval(item.strip())] = 'Response change'
    if 'request' in item.lower():
        unknown_change_mapping[eval(item.strip())] = 'Request change'

# Define function mapper that maps the values of a list using a dictionary

def mapper(mapping, list):
    if not list:
        return []
    mapped_list = [mapping.get(item, "Other") for item in list]
    return mapped_list

# Map breaking_change_ids using mapper function

data['breaking_changes_categories'] = data['breaking_changes_ids'].apply(lambda x: list(set(mapper(breaking_change_mapping, eval(x)))))
data['non_breaking_changes_categories'] = data['non_breaking_changes_ids'].apply(lambda x: list(set(mapper(non_breaking_change_mapping, eval(x)))))
data['unknown_changes_categories'] = data['unknown_changes_ids'].apply(lambda x: list(set(mapper(unknown_change_mapping, eval(x)))))


# Add new column 'API_change', 'Response_change', 'Request_change' to the dataframe

data['Breaking_API_change'] = data.apply(lambda row: 'APIC' if 'API change' in row['breaking_changes_categories'] else 'N-APIC', axis=1)
data['Breaking_Request_change'] = data.apply(lambda row: 'REQC' if 'Request change' in row['breaking_changes_categories'] else 'N-REQC', axis=1)
data['Breaking_Response_change'] = data.apply(lambda row: 'RESC' if 'Response change' in row['breaking_changes_categories'] else 'N-RESC', axis=1)
data['Non-breaking_API_change'] = data.apply(lambda row: 'APIC' if 'API change' in row['non_breaking_changes_categories'] or 'API change' in row['unknown_changes_categories'] else 'N-APIC', axis=1)
data['Non-breaking_Request_change'] = data.apply(lambda row: 'REQC' if 'Request change' in row['non_breaking_changes_categories'] or 'Request change' in row['unknown_changes_categories'] else 'N-REQC', axis=1)
data['Non-breaking_Response_change'] = data.apply(lambda row: 'RESC' if 'Response change' in row['non_breaking_changes_categories'] or 'Response change' in row['unknown_changes_categories'] else 'N-RESC', axis=1)

# Save this dataframe as csv file 

best_scenario = data[['api_spec_id', 'version_change_classification', 'breaking_changes_categories', 'non_breaking_changes_categories', 'unknown_changes_categories', 'current_vc', 'Breaking_API_change', 'Breaking_Response_change', 'Breaking_Request_change', 'Non-breaking_API_change', 'Non-breaking_Response_change', 'Non-breaking_Request_change']]

# Save the new dataframe as csv file 

best_scenario.to_csv('/Users/matteosala/Desktop/Master Management and Informatics/Sem4/Thesis/Dataset/Detailed_version_mid_level_best_scenario.csv', index=False)

data['Breaking_API_change'] = data.apply(lambda row: 'APIC' if 'API change' in row['breaking_changes_categories'] or 'API change' in row['unknown_changes_categories'] else 'N-APIC', axis=1)
data['Breaking_Request_change'] = data.apply(lambda row: 'REQC' if 'Request change' in row['breaking_changes_categories'] or 'Request change' in row['unknown_changes_categories'] else 'N-REQC', axis=1)
data['Breaking_Response_change'] = data.apply(lambda row: 'RESC' if 'Response change' in row['breaking_changes_categories'] or 'Response change' in row['unknown_changes_categories'] else 'N-RESC', axis=1)
data['Non-breaking_API_change'] = data.apply(lambda row: 'APIC' if 'API change' in row['non_breaking_changes_categories'] else 'N-APIC', axis=1)
data['Non-breaking_Request_change'] = data.apply(lambda row: 'REQC' if 'Request change' in row['non_breaking_changes_categories'] else 'N-REQC', axis=1)
data['Non-breaking_Response_change'] = data.apply(lambda row: 'RESC' if 'Response change' in row['non_breaking_changes_categories'] else 'N-RESC', axis=1)

worst_scenario = data[['api_spec_id', 'version_change_classification', 'breaking_changes_categories', 'non_breaking_changes_categories', 'unknown_changes_categories', 'current_vc', 'Breaking_API_change', 'Breaking_Response_change', 'Breaking_Request_change', 'Non-breaking_API_change', 'Non-breaking_Response_change', 'Non-breaking_Request_change']]

worst_scenario.to_csv('/Users/matteosala/Desktop/Master Management and Informatics/Sem4/Thesis/Dataset/Detailed_version_mid_level_worst_scenario.csv', index=False)



