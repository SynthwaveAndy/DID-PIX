# P.O.R.N.O
(Proof of Related NFT Ownership)

## About
This simple script can be used to generate a list of XCH Receive addresses for owners of Chia NFTs in any number listed collections. You can also specify DID's to exclude from the output list (For example, if the collection creator has their own NFT's in their DID).

## Dependancies
- [Python 3.7+](https://www.python.org/downloads/)
- Use `pip install <import>` for any missing imports.

## Customizing
By default and for example, this is configured for the [$DEGEN](https://www.taildatabase.com/tail/320b869bc8d293cca8784187312da1a61cf43b9cf0724b47d8e027dcca1dd501) Airdrop snapshot.

Simply open the `collections.csv` file and add your Collection names and ID's.
Then open the `excluded_DIDs.csv` file and add any DID's you need to exclude.

*Do not modify the file headers (first rows)*

## Running
`$ python porno_snapshot.py`

## Output
This script will produce the following Four output files.
### **nft_ownership.csv**
> *Schema/Header:* `nft_name,nft_id,owner_name,owner_DID,owner_address`

Contains records of all NFT's which are assigned to a DID. This excludes any DIDs listed in `excluded_DIDs.csv`, and includes any "Unclaimed" DIDs on MintGarden - as Denoted by "Unclaimed DID". This is pre-sorted by Owner Name.

### **nft_ownership_agg.csv**
> *Schema/Header:* `owner_name,NFTs_owned_count,owner_DID,owner_address`

Containts aggregations (tallied records) of `nft_ownership.csv` by DID. The Owners XCH Receive Address maintained for this dataset it is simply taken from the first record in `nft_ownership.csv`

### **didless.csv**
> *Schema/Header:* `nft_name,nft_id,owner_address`

The entries in this file represent the NFTs which have not been assigned to a DID (Claimed or Not). Most of these NFTs are simply unsold

### **excluded_NFTs.csv**
> *Schema/Header:* `nft_name,nft_id,owner_name,owner_DID,owner_address`

Contains records of all NFTs belonging to Excluded DIDs

## Credits
Thankfully powered by [MintGarden.io](mintgarden.io) public API.

Not associated with MintGarden.io.

Based on the work of Steve Stepp [xchdev.com](xchdev.com)

## Disclaimer
This software is provided "As Is", it is your responsibility to ensure correctness of data produced.
The author takes no liability for any losses incured.

A lot to do with Chia NFTs, nothing to do with any Hubs..