# Import required libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.neighbors import NearestNeighbors
import scipy.sparse
import os

class PlayerSimilarityModel:
    """
    A machine learning model to find similar football players based on their attributes.
    Uses KNN with cosine similarity to identify players with similar characteristics.
    """
    
    def __init__(self, data_path):
        """
        Initialize the model with data path and preprocessing components.
        
        Args:
            data_path (str): Path to the player data CSV file
        """
        self.data_path = data_path
        self.df = None
        self.transformed_data = None
        self.feature_names = None
        self.column_transformer = None
        self.knn_model = None
        
    def load_and_preprocess_data(self):
        """
        Load data and perform feature engineering steps.
        """
        # Load raw data
        self.df = pd.read_csv(self.data_path)
        
        # Feature engineering
        self.df["id"] = self.df.index
        self.df[["atk_workrate", "def_workrate"]] = self.df["work_rate"].str.split("/", expand=True)
        self.df["def_workrate"] = self.df["def_workrate"].str.strip()
        
        # Define feature groups
        self._define_feature_groups()
        
    def _define_feature_groups(self):
        """
        Define and categorize features for preprocessing.
        """
        self.categorical_features = ["country", "club", "best_position"]
        self.ordinal_features = ["atk_workrate", "def_workrate"]
        self.binary_features = ["preferred_foot"]
        self.drop_features = ["name", "first_name", "last_name", "work_rate", "id"]
        
        # Derive numeric features
        self.numeric_features = list(set(self.df.columns) - 
                                   set(self.categorical_features) - 
                                   set(self.drop_features) -
                                   set(self.binary_features) -
                                   set(self.ordinal_features))
        
    def create_preprocessing_pipeline(self):
        """
        Create and configure the preprocessing pipeline.
        """
        # Define transformers
        numeric_transformer = make_pipeline(StandardScaler())
        categorical_transformer = make_pipeline(
            OneHotEncoder(handle_unknown="ignore")
        )
        ordinal_transformer = make_pipeline(
            OrdinalEncoder(categories=[["High", "Medium", "Low"], 
                                     ["High", "Medium", "Low"]], 
                         dtype=int)
        )
        binary_transformer = make_pipeline(
            OneHotEncoder(drop="if_binary", dtype=int)
        )
        
        # Create column transformer
        self.column_transformer = make_column_transformer(
            (numeric_transformer, self.numeric_features),
            (categorical_transformer, self.categorical_features),
            (ordinal_transformer, self.ordinal_features),
            (binary_transformer, self.binary_features),
            ("drop", self.drop_features)
        )
        
    def fit_transform_data(self):
        """
        Fit the preprocessing pipeline and transform the data.
        """
        transformed = self.column_transformer.fit_transform(self.df)
        if isinstance(transformed, scipy.sparse.spmatrix):
            transformed = transformed.toarray()
            
        # Get feature names
        self.feature_names = (
            self.numeric_features +
            self.column_transformer.named_transformers_["pipeline-2"].get_feature_names_out().tolist() +
            self.column_transformer.named_transformers_["pipeline-4"].get_feature_names_out().tolist() +
            self.ordinal_features
        )
        
        self.transformed_data = pd.DataFrame(transformed, columns=self.feature_names)
        
    def fit_knn_model(self, n_neighbors=5):
        """
        Fit the KNN model for finding similar players.
        
        Args:
            n_neighbors (int): Number of similar players to find
        """
        self.knn_model = NearestNeighbors(
            n_neighbors=n_neighbors + 1,  # +1 because first neighbor is self
            metric="cosine",
            algorithm="brute"
        ).fit(self.transformed_data)
        
    def find_similar_players(self, player_name=None, player_id=None):
        """
        Find similar players based on name or ID.
        
        Args:
            player_name (str, optional): Full name of the player
            player_id (int, optional): ID of the player
            
        Returns:
            pd.DataFrame: DataFrame containing similar players and their attributes
        """
        if player_name:
            player_id = self.df[self.df["name"] == player_name]["id"].iloc[0]
        
        player_vector = self.transformed_data.iloc[player_id].values.reshape(1, -1)
        distances, indices = self.knn_model.kneighbors(player_vector)
        
        # Get similar players' details
        display_cols = ["name", "age", "overall", "potential", "value", 
                       "country", "club", "best_position", "preferred_foot"]
        similar_players = self.df.iloc[indices[0][1:]].reset_index(drop=True)[display_cols]
        similar_players["similarity_score"] = 1 - distances[0][1:]
        
        return similar_players.sort_values("similarity_score", ascending=False)
    

def main():
    """
    Main execution method to demonstrate the player similarity model.
    """
    try:
        # Initialize and use the model
        model = PlayerSimilarityModel("data/raw/player_raw_data.csv")
        model.load_and_preprocess_data()
        model.create_preprocessing_pipeline()
        model.fit_transform_data()
        model.fit_knn_model(n_neighbors=5)

        while True:
            player_name = input("\nEnter player name (or 'quit' to exit): ").strip()
            if player_name.lower() == 'quit':
                break
            
            try:
                similar_players = model.find_similar_players(player_name=player_name)
                print("\nMost similar players to", player_name + ":")
                print(similar_players.to_string(index=False))
            except IndexError:
                print(f"\nError: Player '{player_name}' not found in database.")
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
            
    except FileNotFoundError:
        print("Error: Player database file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()