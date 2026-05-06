import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# LOAD DATA
df = pd.read_csv("weather_classification_data.csv")

# REMOVE EXTRA SPACES SA COLUMN NAMES
df.columns = df.columns.str.strip()

print("\nDATASET COLUMNS:")
print(df.columns)

print("\nSAMPLE DATA:")
print(df.head())

# LABEL ENCODERS
le_cloud = LabelEncoder()
le_season = LabelEncoder()
le_location = LabelEncoder()
le_target = LabelEncoder()

# FIT + TRANSFORM
df['Cloud Cover'] = le_cloud.fit_transform(df['Cloud Cover'])
df['Season'] = le_season.fit_transform(df['Season'])
df['Location'] = le_location.fit_transform(df['Location'])
df['Weather Type'] = le_target.fit_transform(df['Weather Type'])

# PRINT EXACT VALID VALUES
print("\nVALID CLOUD VALUES:")
print(le_cloud.classes_)

print("\nVALID SEASON VALUES:")
print(le_season.classes_)

print("\nVALID LOCATION VALUES:")
print(le_location.classes_)

print("\nVALID TARGET VALUES:")
print(le_target.classes_)

# EXACT FEATURE ORDER
X = df[
[
    'Temperature',
    'Humidity',
    'Wind Speed',
    'Precipitation (%)',
    'Cloud Cover',
    'Atmospheric Pressure',
    'UV Index',
    'Season',
    'Visibility (km)',
    'Location'
]
]

y = df['Weather Type']

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# MODEL
model = DecisionTreeClassifier(
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# ACCURACY
print("\nMODEL ACCURACY:")
print(model.score(X_test, y_test))

# SAVE FILES
joblib.dump(model, "model.pkl")
joblib.dump(le_cloud, "le_cloud.pkl")
joblib.dump(le_season, "le_season.pkl")
joblib.dump(le_location, "le_location.pkl")
joblib.dump(le_target, "le_target.pkl")

print("\nMODEL READY SUCCESSFULLY")