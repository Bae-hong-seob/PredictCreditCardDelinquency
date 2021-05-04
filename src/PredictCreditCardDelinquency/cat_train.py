import argparse

import pandas as pd

from data.dataset import load_dataset
from model.gbdt import stratified_kfold_cat

train, test = load_dataset()
X = train.drop("credit", axis=1)
y = train["credit"]
X_test = test.copy()


if __name__ == "__main__":
    path = "../../input/predict-credit-card-delinquency/"
    parse = argparse.ArgumentParser("Training!")
    parse.add_argument(
        "--path", type=str, help="Input data save path", default="../../submission/"
    )
    parse.add_argument("--file", type=str, help="Input file name", default="model.csv")
    parse.add_argument("--fold", type=int, default=10)
    args = parse.parse_args()

    cat_params = {
        "l2_leaf_reg": 0.08,
        "max_depth": 10,
        "bagging_temperature": 1,
        "min_data_in_leaf": 72,
        "max_bin": 364,
        "random_state": 42,
        "eval_metric": "MultiClass",
        "loss_function": "MultiClass",
        "learning_rate": 0.01,
        "od_type": "Iter",
        "od_wait": 500,
        "n_estimators": 10000,
        "cat_features": [
            "income_type",
            "edu_type",
            "family_type",
            "house_type",
            "occyp_type",
            "gender_car_reality",
        ],
    }

    cat_preds = stratified_kfold_cat(cat_params, args.fold, X, y, X_test)
    submission = pd.read_csv(path + "sample_submission.csv")
    submission.iloc[:, 1:] = cat_preds
    submission.to_csv(args.path + args.file, index=False)