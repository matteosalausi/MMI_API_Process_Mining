#Import csv file

import pandas as pd
import numpy as np

# Load the data

data = pd.read_csv('/Users/matteosala/Desktop/Master Management and Informatics/Sem4/Thesis/Dataset/Detailed_version.csv')

# Check data

print(data.head())

# Drop useless columns

data = data.drop('Unnamed: 0', axis=1)
print(data.head())

# Creating a new dataframe that contains columns api_spec_id, version_change_classification, current_vc called as "date", a new column "breaking" which is True if the breaking_changes_sum is greater than 0.

new_data = data[['api_spec_id', 'version_change_classification', 'current_vc', 'breaking_changes_sum', 'non_breaking_changes_sum', 'unknown_changes_sum']].copy()

# Create new column "change_type"

new_data['change_type'] = np.where(new_data['breaking_changes_sum'] > 0, 'BC', np.where(new_data['non_breaking_changes_sum'] > 0, 'NBC', 'UND'))
print(new_data.head())

# Remove breaking_changes_sum, non_breaking_changes_sum, unknown_changes_sum

new_data = new_data.drop(['breaking_changes_sum', 'non_breaking_changes_sum', 'unknown_changes_sum'], axis=1)
print(new_data.head())

# Save the new dataframe as csv file over the /Users/matteosala/Desktop/Master Management and Informatics/Sem4/Thesis/Dataset directory

new_data.to_csv('/Users/matteosala/Desktop/Master Management and Informatics/Sem4/Thesis/Dataset/Preprocessed_data.csv', index=False)


