import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors

class PlayerSimilarityModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.transformed_data = None
        self.feature_names = None
        self.column_transformer = None
        self.knn_model = None

    def load_and_preprocess_data(self):
        self.df = pd.read_csv(self.data_path)
        self.df["id"] = self.df.index
        self.df[["atk_workrate", "def_workrate"]] = self.df["work_rate"].str.split("/", expand=True)
        self.df["def_workrate"] = self.df["def_workrate"].str.strip()
        self._define_feature_groups()

    def _define_feature_groups(self):
        self.categorical_features = ["country", "club", "best_position"]
        self.ordinal_features = ["atk_workrate", "def_workrate"]
        self.binary_features = ["preferred_foot"]
        self.drop_features = ["name", "first_name", "last_name", "work_rate", "id"]
        self.numeric_features = list(set(self.df.columns) - 
                                     set(self.categorical_features) - 
                                     set(self.drop_features) -
                                     set(self.binary_features) -
                                     set(self.ordinal_features))

    def create_preprocessing_pipeline(self):
        numeric_transformer = Pipeline([
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline([
            ('onehot', OneHotEncoder(handle_unknown="ignore"))
        ])
        ordinal_transformer = Pipeline([
            ('ordinal', OneHotEncoder(drop="if_binary"))
        ])
        binary_transformer = Pipeline([
            ('binary', OneHotEncoder(drop="if_binary"))
        ])

        self.column_transformer = ColumnTransformer([
            ('num', numeric_transformer, self.numeric_features),
            ('cat', categorical_transformer, self.categorical_features),
            ('ord', ordinal_transformer, self.ordinal_features),
            ('bin', binary_transformer, self.binary_features)
        ])

    def fit_transform_data(self):
        self.transformed_data = self.column_transformer.fit_transform(self.df)
        self.feature_names = (
            self.numeric_features +
            self.column_transformer.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(self.categorical_features).tolist() +
            self.column_transformer.named_transformers_['ord'].named_steps['ordinal'].get_feature_names_out(self.ordinal_features).tolist() +
            self.column_transformer.named_transformers_['bin'].named_steps['binary'].get_feature_names_out(self.binary_features).tolist()
        )

    def fit_knn_model(self, n_neighbors=5):
        self.knn_model = NearestNeighbors(
            n_neighbors=n_neighbors + 1,
            metric="cosine",
            algorithm="brute"
        ).fit(self.transformed_data)

    def find_similar_players(self, player_name):
        player_id = self.df[self.df["name"].str.lower() == player_name.lower()]["id"].iloc[0]
        player_vector = self.transformed_data[player_id].reshape(1, -1)
        distances, indices = self.knn_model.kneighbors(player_vector)

        display_cols = ["name", "age", "overall", "potential", "value", 
                        "country", "club", "best_position", "preferred_foot"]
        similar_players = self.df.iloc[indices[0][1:]].reset_index(drop=True)[display_cols]
        similar_players["similarity_score"] = 1 - distances[0][1:]

        return similar_players.sort_values("similarity_score", ascending=False).to_dict('records')

