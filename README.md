# DID PIX

Version 1.1.0

<div align="center">
    <img src="https://bafybeiam6rq5c5jmg5lp524q6elln33stojpsclipzr5whicyegmzmfdym.ipfs.nftstorage.link/DIDPIX.png" style="width:40%;height:auto;"/>
    <p><a href="https://mintgarden.io/nfts/nft1frue7ehxrj975q3dy9f8n0lq0a7lt7676jlg5rl59yr2dzc2y46qdksvxk">Johnson Peeperton</a> the DID PIX Mascot!</p>
</div>

## About

This simple program can be used to generate a list of XCH Receive addresses for owners of Chia NFTs in any number given collections. You can also specify DID's to exclude from the output list (For example, if the collection creator has their own NFT's in their DID).

> Note: In previous versions of this tool, you would edit CSV Files to list the collections and excluded DIDs, this is now handled via a novel menu implementation.

## Dependancies

- [Python 3.7+](https://www.python.org/downloads/)
- Use `pip install <import>` for any missing imports.

## Example

Included for example, is the output for the `Proof of Synth and Time` NFT collection, as of the day of this commit.

## Running

`$ python didpix.py`

## Output

This program will produce the following 4 output files.

### **nft_ownership.csv**

> *Schema/Header:* `nft_name,nft_id,owner_name,owner_DID,owner_address`

Contains records of all NFT's which are assigned to a DID. This excludes any DIDs provided, and includes any "Unclaimed" DIDs on MintGarden - as Denoted by "Unclaimed DID". This is pre-sorted by Owner Name.

### **nft_ownership_agg.csv**

> *Schema/Header:* `owner_name,NFTs_owned_count,owner_DID,owner_address`

Contains aggregations (tallied records) of `nft_ownership.csv` by DID. The Owners XCH Receive Address maintained for this dataset it is simply taken from the first record in `nft_ownership.csv`

### **DIDless.csv**

> *Schema/Header:* `nft_name,nft_id,owner_address`

The entries in this file represent the NFTs which have not been assigned to a DID (Claimed or Not). Most of these NFTs are simply unsold

### **excluded_NFTs.csv**

> *Schema/Header:* `nft_name,nft_id,owner_name,owner_DID,owner_address`

Contains records of all NFTs belonging to Excluded DIDs

## Support Development

- If you would like to support future development of this tool, or tools like it, consider buying a [ChiFi Degen](https://dexie.space/offers/col1cueue8anxk6uyf0gu92gwxfm2myf7mdq06z744h32wlw37urhlvsjnpu9c/xch) :D
- Please provide `feature requests` or report `issues` in the Issues tab on GitHub.
- Want to ask a question, get help or provide feedback? Join my [Discord]() server.

## Credits

Thankfully powered by [MintGarden.io](mintgarden.io) public API.

> Not associated with MintGarden.io.

## Disclaimer

This software is provided "As Is", it is your responsibility to ensure correctness of data produced.
The author takes no liability for any losses incurred.
