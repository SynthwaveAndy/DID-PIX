import requests
from dataclasses import dataclass
import csv
import time

# Proof of Related NFT Ownership (P.O.R.N.O)
# Thank you to MintGarden.io for providing the API which makes this an easy task!


# Reads names and id's from csv files, and returns them as in a list
def read_config(filename : str):
    read_list = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader) # Ignore the Header Line
        for row in csvreader:
            read_list.append({'name' : row[0], 'id' : row[1]})
    return read_list

applicable_collections = read_config('collections.csv')
excluded_DIDs = read_config('excluded_DIDs.csv')

# Add a counter for excluded DIDs
for ed in excluded_DIDs:
    ed['total_excluded'] = 0



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

nfts = []



## Get all potentially applicable NFT IDs from listed collections
collection_index = 1
for collection in applicable_collections:
    print("\n", collection_index, "/", len(applicable_collections), " Fetching NFT IDs for:", collection['name'])

    resp = requests.get(url=f'https://api.mintgarden.io/collections/{collection["id"]}/nfts/ids')
    data = resp.json()

    for d in data:
        nfts.append(NFT(d['name'], d['encoded_id'], None))

    print(len(data), " NFTs located for ", collection['name'])
    collection_index += 1

print("\n", len(nfts), " NFTs located in Total\n")



## Helper function for generating progress bars    
# Print iterations progress
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#', printEnd = "\r"):
    total = len(iterable)
    
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        
    # Initial Call
    printProgressBar(0)
    
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
        
    # Print New Line on Complete
    print()



# Define a sorting key function that extracts the owner name from NFT data
def get_owner_did(nft):
    return nft.owner.did

 

if len(nfts) > 0:
    # Create the Output files as per the README.md
    nft_ownership_file = open("./Output/nft_ownership.csv", 'w', encoding="utf-8", newline='')
    nft_ownership_writer = csv.writer(nft_ownership_file, delimiter =',')

    nft_ownership_agg_file = open("./Output/nft_ownership_agg.csv", 'w', encoding="utf-8", newline='')
    nft_ownership_agg_writer = csv.writer(nft_ownership_agg_file, delimiter =',')

    didless_file = open("./Output/didless.csv", 'w', encoding="utf-8", newline='')
    didless_writer = csv.writer(didless_file, delimiter =',')

    excluded_NFTs_file = open("./Output/excluded_NFTs.csv", 'w', encoding="utf-8", newline='')
    excluded_NFTs_writer = csv.writer(excluded_NFTs_file, delimiter =',')

    # Write the csv headers
    nft_ownership_writer.writerow(['nft_name','nft_id','owner_name','owner_DID','owner_address'])
    nft_ownership_agg_writer.writerow(['owner_name','NFTs_owned_count','owner_DID','owner_address'])
    didless_writer.writerow(['nft_name','nft_id','owner_address'])
    excluded_NFTs_writer.writerow(['nft_name','nft_id','owner_name','owner_DID','owner_address'])



    ## Get Owner addresses for each NFT
    did_assigned_nfts = []
    for nft in progressBar(nfts, prefix = 'Fetching Wallet Addresses:', suffix = 'Complete', length = 32):
        try:
            resp = requests.get(url=f'https://api.mintgarden.io/nfts/{nft.id}')
            data = resp.json()
        except:
            # If request has failed or timed out, try again after wait.
            print(f'\nFetching: {nft.id} failed. Trying again in 5 seconds', end='')
            for s in range(5):
                time.sleep(s)
                print(".", end="")
            resp = requests.get(url=f'https://api.mintgarden.io/nfts/{nft.id}')
            data = resp.json()

        xch_address = data["owner_address"]["encoded_id"]

        if data["owner"]:
            nft.owner = Owner(data["owner"]["name"], data["owner"]["encoded_id"], xch_address)
            if not nft.owner.name:
                nft.owner.name = "Unclaimed DID"
        else:
            # The NFT is not assigned to a DID
            didless_writer.writerow([nft.name, nft.id, xch_address])
            continue
        
        rejected = False
        for excluded_DID in excluded_DIDs:
            if nft.owner.did == excluded_DID['id']:
                excluded_NFTs_writer.writerow([nft.name, nft.id, nft.owner.name, nft.owner.did, nft.owner.address])
                excluded_DID['total_excluded'] += 1
                rejected = True

        if not rejected:
            did_assigned_nfts.append(nft)
            

    # Sort the list of NFTs by owner name
    sorted_nfts = sorted(did_assigned_nfts, key=get_owner_did)

    # Write the sorted list of NFTs
    for nft in progressBar(sorted_nfts, prefix = 'Writing sorted list of Owned NFTs:', suffix = 'Complete', length = 32):
        nft_ownership_writer.writerow([nft.name, nft.id, nft.owner.name, nft.owner.did, nft.owner.address])
    
    owner_names = []
    counts = []
    owner_dids = []
    owner_addresses = []
    # Aggregate the List
    for nft in progressBar(sorted_nfts, prefix = 'Writing aggregated list of Owners:', suffix = 'Complete', length = 32):
        if nft.owner.did in owner_dids:
            counts[owner_dids.index(nft.owner.did)] += 1
        else:
            owner_names.append(nft.owner.name)
            counts.append(1)
            owner_dids.append(nft.owner.did)
            owner_addresses.append(nft.owner.address)
    
    # Write the aggregated list
    for i in range(len(owner_names)):
        nft_ownership_agg_writer.writerow([owner_names[i], counts[i], owner_dids[i], owner_addresses[i]])

    print("\nTotal of ", len(sorted_nfts), " verifiably owned NFTs found")

    # Close files
    nft_ownership_file.close()
    nft_ownership_agg_file.close()
    didless_file.close()
    excluded_NFTs_file.close()

else:
    print("\nMintGarden API failed to return valid collection responses")

# As this script can take a while, alert the user with a system alarm
print('\nSnapshot Complete!\a')