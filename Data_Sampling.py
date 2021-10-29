import pandas as pd
loaded_data = pd.read_csv("cleaned_source_target_category.csv")
data = loaded_data.sample(n = 1000000)
data.to_csv('sample_cleaned_source_target_category.csv', index=False)
