import pandas as pd

# File paths
men_final = "H:/NCAA March Madness 2025/csv/FinalSubmission2.csv"
women_final = "H:/NCAA March Madness 2025/csv/Kaggle v5 - Sheet8.csv"
men_kaggle = "H:/NCAA March Madness 2025/csv/bquxjob_738d4d70_195b217094e.csv"
women_kaggle = "H:/NCAA March Madness 2025/csv/bquxjob_4d305243_195b2173848.csv"

# Load model-generated predictions
final_men = pd.read_csv(men_final)
final_women = pd.read_csv(women_final)

# Load Kaggle-required templates
kaggle_men = pd.read_csv(men_kaggle)
kaggle_women = pd.read_csv(women_kaggle)

# Combine men's and women's predictions
final_preds = pd.concat([final_men, final_women], ignore_index=True)

# Combine men's and women's Kaggle templates
kaggle_template = pd.concat([kaggle_men, kaggle_women], ignore_index=True)

# Merge, replacing Kaggle's 0.5 values with model predictions where available
merged_df = kaggle_template.set_index("ID").combine_first(final_preds.set_index("ID")).reset_index()

# Save final submission file
merged_df.to_csv("H:/NCAA March Madness 2025/csv/Kaggle_HighConfidence_submission.csv", index=False)

print("Final Kaggle submission file saved as 'submission.csv'!")
