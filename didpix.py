from utils import ProgressBar, System, Log, Color
from query_user import QueryUser

from dataclasses import dataclass
from typing import List

import requests
import csv
import time


## The classes which will store the downloaded data
@dataclass
class Owner:
    name: str
    did: str
    address: str

@dataclass
class NFT:
    name: str
    id: str
    owner: Owner
    

def display_title():
    print("\t ___   _  ___       ___  _ __  _ \n" +
      "\t| . \ | || . \     | . \| |\ \/  \n" +
      "\t| |  || || |  | 📷 |  _/| | \ \  \n" + 
      "\t|___/ |_||___/     |_|  |_|_/\_\ ")


def mint_garden_get_request(url_request : str, allow_timeout : bool = False) -> dict:
    try:
        resp = requests.get(url=url_request, timeout=5.0)
        resp.raise_for_status()  # Raise an exception if the request was unsuccessful
        data = resp.json()
        
        return data
        
    except requests.exceptions.ConnectionError as e:
        Log.ERR("Could not connect to MintGarden API. Please check your internet connection.")
        System.exit("Please fix your internet connection, and try again.")
        
    except requests.exceptions.Timeout as e:
        Log.ERR("The request to MintGarden API timed out, the server may be down or extremely busy.")
        if not allow_timeout:
            System.exit("Please try again later.")
        
    except requests.exceptions.RequestException as e:
        Log.ERR(f"Error occurred while making the request: {e}")
        
    except ValueError as e:
        Log.ERR(f"Error occurred while parsing the response: {e}")


def fetch_collection_name(collection_id : str) -> str:
    data = mint_garden_get_request(f'https://api.mintgarden.io/collections/{collection_id}')
    
    if data and 'name' in data.keys():
        return data['name']
    
    return ""
    

## Get all potentially NFT IDs from given collections
def fetch_NFT_IDs(collections : List[str]) -> List[NFT]:
    Log.INFO("Fetching all NFT IDs for all Collections")
    nfts = []
    
    collection_index = 1
    for col in collections:
        print()
        Log.INFO(f"{collection_index}/{len(collections)} Fetching NFT IDs for: {col['name']}")

        resp = requests.get(url=f'https://api.mintgarden.io/collections/{col["ID"]}/nfts/ids')
        data = resp.json()

        for d in data:
            nfts.append(NFT(d['name'], d['encoded_id'], None))

        log_msg = f"{len(data)} NFTs located for {col['name']}"
        if len(data) > 0:
            Log.PASS(log_msg)
        else:
            Log.WARN(log_msg)
            
        collection_index += 1

    print()
    log_msg = f"{len(nfts)} NFTs located in total for all collections\n"
    if len(nfts) > 0:
        Log.PASS(log_msg)
    else:
        Log.WARN(log_msg)

    return nfts


# Define a sorting key function that extracts the owner name from NFT data
def get_owner_did(nft : NFT) -> str:
    return nft.owner.did


def generate_results(nfts : List[NFT], excluded_DIDs : List[dict]):
    Log.INFO("Creating and Opening the output files")
    # Create the Output files as per the README.md
    nft_ownership_file = open("./Output/nft_ownership.csv", 'w', encoding="utf-8", newline='')
    nft_ownership_writer = csv.writer(nft_ownership_file, delimiter =',')

    nft_ownership_agg_file = open("./Output/nft_ownership_agg.csv", 'w', encoding="utf-8", newline='')
    nft_ownership_agg_writer = csv.writer(nft_ownership_agg_file, delimiter =',')

    DIDless_file = open("./Output/DIDless.csv", 'w', encoding="utf-8", newline='')
    DIDless_writer = csv.writer(DIDless_file, delimiter =',')

    excluded_NFTs_file = open("./Output/excluded_NFTs.csv", 'w', encoding="utf-8", newline='')
    excluded_NFTs_writer = csv.writer(excluded_NFTs_file, delimiter =',')

    # Write the csv headers
    nft_ownership_writer.writerow(['nft_name','nft_id','owner_name','owner_DID','owner_address'])
    nft_ownership_agg_writer.writerow(['owner_name','NFTs_owned_count','owner_DID','owner_address'])
    DIDless_writer.writerow(['nft_name','nft_id','owner_address'])
    excluded_NFTs_writer.writerow(['nft_name','nft_id','owner_name','owner_DID','owner_address'])


    ## Get Owner addresses for each NFT
    did_assigned_nfts = []
    for nft in ProgressBar.create(nfts, prefix = 'Fetching Wallet Addresses:', suffix = Color.green_text('Done!'), length = 25):
        try:
            data = mint_garden_get_request(url_request=f'https://api.mintgarden.io/nfts/{nft.id}', allow_timeout=True)
        except:
            # If request has failed or timed out, try again after wait.
            Log.NOTE(f'\nFetching: {nft.id} failed. Trying again in 5 seconds', end='')
            for s in range(5):
                time.sleep(s)
                print(".", end="")
            data = mint_garden_get_request(url_request=f'https://api.mintgarden.io/nfts/{nft.id}', allow_timeout=False)

        xch_address = data["owner_address"]["encoded_id"]

        if data["owner"]:
            nft.owner = Owner(data["owner"]["name"], data["owner"]["encoded_id"], xch_address)
            if not nft.owner.name:
                nft.owner.name = "Unclaimed DID"
        else:
            # The NFT is not assigned to a DID
            DIDless_writer.writerow([nft.name, nft.id, xch_address])
            continue
        
        rejected = False
        for excluded_DID in excluded_DIDs:
            if nft.owner.did == excluded_DID['ID']:
                excluded_NFTs_writer.writerow([nft.name, nft.id, nft.owner.name, nft.owner.did, nft.owner.address])
                excluded_DID['total_excluded'] += 1
                rejected = True

        if not rejected:
            did_assigned_nfts.append(nft)
            
    # Sort the list of NFTs by owner name
    sorted_nfts = sorted(did_assigned_nfts, key=get_owner_did)

    # Write the sorted list of NFTs
    for nft in ProgressBar.create(sorted_nfts, prefix = 'Writing sorted list of Owned NFTs:', suffix = Color.green_text('Done!'), length = 17):
        nft_ownership_writer.writerow([nft.name, nft.id, nft.owner.name, nft.owner.did, nft.owner.address])
    
    owner_names = []
    counts = []
    owner_DIDs = []
    owner_addresses = []
    
    # Aggregate the List
    for nft in ProgressBar.create(sorted_nfts, prefix = 'Writing aggregated list of Owners:', suffix = Color.green_text('Done!'), length = 17):
        if nft.owner.did in owner_DIDs:
            counts[owner_DIDs.index(nft.owner.did)] += 1
        else:
            owner_names.append(nft.owner.name)
            counts.append(1)
            owner_DIDs.append(nft.owner.did)
            owner_addresses.append(nft.owner.address)
    
    # Write the aggregated list
    for i in range(len(owner_names)):
        nft_ownership_agg_writer.writerow([owner_names[i], counts[i], owner_DIDs[i], owner_addresses[i]])

    Log.PASS(f"Total of {len(sorted_nfts)} verifiably owned NFTs found")

    # Close files
    nft_ownership_file.close()
    nft_ownership_agg_file.close()
    DIDless_file.close()
    excluded_NFTs_file.close()
    
    print()
    Log.PASS("The DID Snapshot is complete!")


def say_goodbye():
    print(f"\n\t  {Color.green_text('Thank you for using DID PIX!')}\n")
    print("Please,\n - Provide Feedback, Feature Requests or report Issues on GitHub")
    print(" - Consider supporting my collections which fuel development of tools like this!")
    input(f"\n {Color.prompt()} Press Enter to exit application..")


def is_ID_duplicate(new_id : str, list : List[dict]) -> bool:
    for l in list:
        if l["ID"] == new_id:
            print()
            Log.NOTE("This ID has already been added to the list.")
            return True
    return False


def verify_collection_ID(collection_id: str, collections : List[dict]):
    print()
    Log.INFO(f"Verifying that {collection_id} exists.")
    name = fetch_collection_name(collection_id)
    
    if name == "":
        Log.ERR(f"Collection with ID of {collection_id} does not exist on MintGarden")
    else:
        collections.append({"ID":collection_id, "name":name})
    Log.PASS(f"{name} has been verified to exist, and added to the list.")



def main():
    System.clear()
    display_title()
    
    print(f"\n{Color.white_highlight(' Page 1/3 : Collection Information')}")
    
    collections = []
    collection_id = QueryUser.get_collection_id("What is the ID of the collection you would like to take a snapshot for?")
    verify_collection_ID(collection_id, collections)
    while (QueryUser.get_bool("Do you have another collection to add to the list?")):
        
        collection_id = QueryUser.get_collection_id("What is the collection ID?")
        if not is_ID_duplicate(collection_id, collections):
            verify_collection_ID(collection_id, collections)
    
    System.clear()
    display_title()

    print(f"\n{Color.white_highlight(' Page 2/3 : DID Exclusion')}")

    # Get the DIDs to exclude from the snapshot
    excluded_DIDs = []
    if (QueryUser.get_bool("Is there any DIDs that you would like to exclude?")):
        excluded_DIDs.append({"ID":QueryUser.get_DID("What is the first DID?"), "name":""})
        excluded_DIDs[len(excluded_DIDs) - 1]['name'] = input(f"\n  {Color.prompt()} Enter a name for this DID: ")
        
        while (QueryUser.get_bool("Do you have another DID to add to the list?")):
            new_DID = QueryUser.get_DID("What is the DID?")
            
            if not is_ID_duplicate(new_DID, excluded_DIDs):
                name = input(f"\n  {Color.prompt()} Enter a name for this DID: ")
                if name == "": name == "Unnamed Excluded DID"
                
                excluded_DIDs.append({"ID":new_DID, "name": name})
    
    # Add a counter to each excluded DID
    for ed in excluded_DIDs:
        ed['total_excluded'] = 0
    
    System.clear()
    display_title()
    
    print(f"\n{Color.white_highlight(' Page 3/3 : DID Snapshot ')}\n")
    
    nfts = fetch_NFT_IDs(collections)
    
    if len(nfts) > 0:
        generate_results(nfts, excluded_DIDs)
    elif len(collections) > 1 :
        Log.ERR("No NFTs were located for any of the provided collections.")
        System.exit("Please ensure that the collection IDs are correct, and that they contain NFTs.")
    else:
        Log.ERR("No NFTs were located for", collections[0]['name'])
        System.exit("Please ensure that the collection ID is correct, and that it contains NFTs.")
        
    input(f"\n {Color.prompt()} Press Enter to continue..")
        
    System.clear()
    display_title()
    
    say_goodbye()
        
        
if __name__ == "__main__":
    main()
