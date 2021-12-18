#!/usr/bin/env python
"""
Performs basic cleaning on the data and saves the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Getting artifact")
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Reading data")
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    logger.info("Dropping Outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Save
    logger.info("Saving cleaned data")
    df.to_csv(path_or_buf="clean_sample.csv", index=False)

    # Upload to wandb
    logger.info("Uploading artifact (cleaned data) to wandb")
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    logger.info("Uploading to wandb successful")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output artifact",
        required=True
    )
    
    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to limit the price column",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maxumum price used to limit the price column",
        required=True
    )

    args = parser.parse_args()

    go(args)
