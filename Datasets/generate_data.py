"""To generate the simulated data"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to generate random timestamps
def generate_random_timestamps(start, end, n_samples):
    """Generate random timestamps"""
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

# Parameters
n = 200000
user_ids = np.arange(1, 80000)  # fewer unique users to allow duplicates
ad_types = np.random.choice(list(range(101, 201)) , n)
event_types = ['impression', 'click']
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 7, 30)
required_date = datetime(2024, 6, 24)

# Generate random data
np.random.seed(42)
data = {
    'user_id': np.random.choice(user_ids, n),
    'timestamp': generate_random_timestamps(pd.to_datetime(start_date), pd.to_datetime(end_date), n),
    'event_type': np.random.choice(event_types, n, p=[0.7, 0.3]),  # adjusted probabilities
    'ad_id': ad_types,
    'revenue': np.round(np.random.normal(10, 5, n), 2)  # adjusted mean revenue to reduce zero occurrences
}

# Ensure revenue is non-negative
data['revenue'] = np.where(data['revenue'] < 0, 0, data['revenue'])

# Convert user_id to object
data['user_id'] = data['user_id'].astype(object)
# Create DataFrame
df = pd.DataFrame(data)

# Ensure all users have at least one record before 2024-06-24
users = df['user_id'].unique()
pre_required_date_df = pd.DataFrame({
    'user_id': users,
    'timestamp': pd.to_datetime([required_date - timedelta(days=1)] * len(users)),
    'event_type': ['impression'] * len(users),  # default to 'impression' for consistency
    'ad_id': np.random.choice(ad_types, len(users)),
    'revenue': np.round(np.random.normal(10, 5, len(users)), 2)
})

# Ensure revenue is non-negative
pre_required_date_df['revenue'] = np.where(pre_required_date_df['revenue'] < 0, 0, pre_required_date_df['revenue'])

# Append this data to the main DataFrame
df = pd.concat([df, pre_required_date_df], ignore_index=True)

# Introduce some duplicates
duplicate_rows = df.sample(frac=0.05, random_state=42)  # 5% duplicates
df = pd.concat([df, duplicate_rows])

# Add more impressions
df.loc[np.random.choice(df.index, 2000), 'event_type'] = 'impression'

# Save to CSV
df.to_csv("Datasets/marketing_campaign_tracking_events_large.csv", index=False)
print('Data generated')
