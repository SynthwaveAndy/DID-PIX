import requests
from utils import System, Formatter, Color
from query_user import QueryUser
import pandas as pd
import numpy as np
import argparse


def display_title():
    print(
        "\n" +
        "\t ___   _  ___       ___  _ __  _ \n" +
        "\t| . \\ | || . \\     | . \\| |\\ \\// \n" +
        "\t| |  || || |  | 📷 |  _/| |/\\ \\  \n" +
        "\t|___/ |_||___/     |_|  |_|_/\\_\\ \n")


def parse_args():
    parser = argparse.ArgumentParser(description="A tool for NFTs on Chia")
    parser.add_argument(
        "-c",
        "--collection_id",
        type=str,
        required=False,
        help="Collection ID")
    return parser.parse_args()


def fetch_collection_name(collection_id: str) -> str:
    try:
        response = requests.get(
            f"https://api.mintgarden.io/collections/{collection_id}")
        # Raise an HTTPError if the status code is >= 400.
        response.raise_for_status()
        page_data = response.json()
        return page_data['name']
    except requests.exceptions.RequestException as e:
        #print(f"An error occurred while making a request to the API: {e}")
        return ""


def fetch_data(collection_id: str, require_owners: bool) -> dict:
    """
    Fetch data from the API and return it as a dictionary.
    """
    data = {"items": []}
    params = {
        "require_owner": str(require_owners).lower(),
        "require_price": "false",
        "size": "100"}

    while True:
        try:
            response = requests.get(
                f"https://api.mintgarden.io/collections/{collection_id}/nfts",
                params=params)
            # Raise an HTTPError if the status code is >= 400.
            response.raise_for_status()
            page_data = response.json()
            if not page_data["items"]:  # Check if the page has no items
                break
            data["items"].extend(page_data["items"])
            if "next" not in page_data:
                break
            params["page"] = page_data["next"]
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making a request to the API: {e}")
            break
    return data


def create_csv_files(collection_id: str, require_owners: bool):
    """
    Fetch data from the API, extract required fields, and create three CSV files.
    """
    # Fetch data from the API
    data = fetch_data(collection_id, require_owners)

    # Extract the required fields from the API response
    nft_ownership_data = [{'encoded_id': item['encoded_id'],
                           'name': item['name'],
                           'owner_name': item['owner_name'],
                           'owner_encoded_id': item['owner_encoded_id'],
                           'owner_address_encoded_id': item['owner_address_encoded_id']} for item in data['items']]

    nft_ownership_agg_data = [{'owner_name': item['owner_name'],
                               'owner_encoded_id': item['owner_encoded_id'],
                               'count_owner_encoded_id': item['owner_encoded_id'],
                               'owner_address_encoded_id': item['owner_address_encoded_id']} for item in data['items']]

    didless_data = [{'name': item['name'],
                     'encoded_id': item['encoded_id'],
                     'owner_address_encoded_id': item['owner_address_encoded_id']} for item in data['items'] if not item['owner_encoded_id']]

    # TODO
    excluded_nfts_data = []

    # Create DataFrame from extracted data
    nft_ownership_df = pd.DataFrame(nft_ownership_data)
    nft_ownership_agg_df = pd.DataFrame(nft_ownership_agg_data)
    didless_df = pd.DataFrame(didless_data)
    excluded_nfts_df = pd.DataFrame(excluded_nfts_data)

    # # Group by owner_name and calculate the counts for nft_ownership_agg.csv then create nft_ownership.csv
    nft_ownership_agg_df["count_owner_encoded_id"] = nft_ownership_agg_df.groupby(
        'owner_encoded_id')['owner_encoded_id'].transform('count')
    nft_ownership_agg_df = nft_ownership_agg_df.drop_duplicates(
        subset=['owner_encoded_id'])
    
    # Replace empty cells with NaN
    nft_ownership_agg_df.replace('', np.nan, inplace=True)
    nft_ownership_agg_df = nft_ownership_agg_df.dropna(
        subset=['owner_encoded_id'])
    nft_ownership_df.to_csv('Output/nft_ownership.csv', index=False)

    # Create nft_ownership_agg.csv
    nft_ownership_agg_df.to_csv('Output/nft_ownership_agg.csv', index=False)

    # Create DIDless.csv
    didless_df.to_csv('Output/DIDless.csv', index=False)

    # Create excluded_nfts.csv
    excluded_nfts_df.to_csv('Output/excluded_NFTs.csv', index=False)


def say_goodbye():
    print(f"\n\t  {Color.green_text('Thank you for using DID PIX!')}\n")
    print("Please,\n - Provide Feedback, Feature Requests or report Issues on GitHub")
    print(" - Consider supporting my collections which fuel development of tools like this!")


def get_collection_info(collection_id_list):
    # Page 1: Collection Information
    Formatter.info("Page 1/3: Collection Information")

    #print(f"\n{Color.white_highlight('Page 1/3: Collection Information')}")

    while True:
        collection_id = QueryUser.get_collection_id(
            "What is the ID of the collection you would like to take a snapshot for?")

        if fetch_collection_name(collection_id):
            collection_id_list.append(collection_id)
            break
        else:
            print("\nCollection ID not found, please check and re-enter")

    # Add more collections if needed
    while QueryUser.get_bool(
            "Do you have another collection to add to the list?"):
        collection_id = QueryUser.get_collection_id(
            "What is the collection ID?")
        if collection_id in collection_id_list:
            print("Collection ID already added.")
        elif fetch_collection_name(collection_id):
            collection_id_list.append(collection_id)
        else:
            print("\nCollection ID not found, please check and re-enter")


def get_did_exculsions(excluded_dids):
    # Page 2: DID Exclusion
    if QueryUser.get_bool("Is there any DIDs that you would like to exclude?"):
        excluded_dids.append({"ID": QueryUser.get_did(
            "What is the first DID?"), "name": ""})
        while QueryUser.get_bool(
                "Do you have another DID to add to the list?"):
            new_did = QueryUser.get_did("What is the DID?")
            if new_did in excluded_dids:
                print("You already entered this DID")
            else:
                excluded_dids.append(new_did)


def did_snapshot(collection_id_list):
    Formatter.info("Creating and Opening the output files")
    for collection in collection_id_list:
        create_csv_files(collection, False)
        print(f"{Color.green_highlight('COLLECTION ')}{collection}")
        Formatter.success("The DID Snapshot is complete!")
        print("\n")


def did_wizard():
    # Call necessary functions to clear screen and display title
    System.clear()
    display_title()

    collection_id_list = []
    excluded_dids = []

    get_collection_info(collection_id_list=collection_id_list)
    get_did_exculsions(excluded_dids=excluded_dids)

    # Call necessary functions to clear screen and display title
    System.clear()
    display_title()

    # Perform DID snapshot for the collection ID list
    print(f"\n{Color.white_highlight(' Page 3/3 : DID Snapshot ')}\n")
    did_snapshot(collection_id_list)
    input(f"\n {Color.prompt()} Press Enter to continue..")

    # Call necessary functions to clear screen and display title
    System.clear()
    display_title()

    # Say goodbye
    say_goodbye()
    input(f"\n {Color.prompt()} Press Enter to exit application..")


def main():
    # Parse command-line arguments#
    args = parse_args()

    if args.collection_id:
        # If collection_id is provided, directly call did_snap() with the
        # provided value
        display_title()
        collection_id = args.collection_id
        did_snapshot([collection_id])
        say_goodbye()
    else:
        did_wizard()


if __name__ == "__main__":
    main()
