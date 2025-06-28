
from Bio import Entrez
import time
import json
from pathlib import Path
from xml.etree import ElementTree as ET

# === CONFIG ===
Entrez.email = "cubasiseko@outlook.com"
Entrez.api_key = "a72c47e71c0e8e878096af6e6529c66e1b08"
Entrez.tool = "BiomedicalLiteratureSentimentAnalyzer"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "pubmed"
DATA_DIR.mkdir(parents=True, exist_ok=True)

QUERY = "cancer immunotherapy"
ID_FILE = DATA_DIR / "pmids.json"
DATA_FILE = DATA_DIR / "pubmed_abstracts.jsonl"
LOG_FILE = DATA_DIR / "progress.log"
ID_LOG_FILE = DATA_DIR / "id_fetch_progress.log"

MAX_PMIDS = 10000
BATCH_SIZE = 200
SLEEP_BETWEEN_CALLS = 0.1

def fetch_all_pmids(query, max_results=MAX_PMIDS):
    print("🔍 Fetching PMIDs...")
    ids = []
    start = 0

    if ID_LOG_FILE.exists():
        with open(ID_LOG_FILE) as f:
            start = int(f.read())
        print(f"⏩ Resuming PMID fetch from offset {start}")

    for offset in range(start, max_results, 10000):
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=10000, retstart=offset)
            record = Entrez.read(handle)
            ids.extend(record["IdList"])
            print(f"✅ Fetched PMIDs {offset}–{offset + len(record['IdList'])}")
            with open(ID_LOG_FILE, "w") as f:
                f.write(str(offset + 10000))
            time.sleep(SLEEP_BETWEEN_CALLS)
            if len(record["IdList"]) < 10000:
                break
        except Exception as e:
            print(f"❌ Error fetching PMIDs at offset {offset}: {e}")
            time.sleep(5)
            continue

    if ids:
        with open(ID_FILE, "w") as f:
            json.dump(ids, f)
        print(f"💾 Saved total PMIDs: {len(ids)}")

    return ids

def load_pmids():
    if ID_FILE.exists():
        with open(ID_FILE) as f:
            return json.load(f)
    return fetch_all_pmids(QUERY)

def load_progress():
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return int(f.read())
    return 0

def save_progress(index):
    with open(LOG_FILE, "w") as f:
        f.write(str(index))

def parse_pubmed_article(xml_entry):
    try:
        article = {}
        medline = xml_entry.get("MedlineCitation", {})
        article_data = medline.get("Article", {})

        article["pmid"] = medline.get("PMID")
        article["title"] = article_data.get("ArticleTitle")

        abstract_text = article_data.get("Abstract", {}).get("AbstractText")
        if isinstance(abstract_text, list):
            article["abstract"] = " ".join(abstract_text)
        else:
            article["abstract"] = abstract_text

        authors = []
        for author in article_data.get("AuthorList", []):
            fname = author.get("ForeName", "")
            lname = author.get("LastName", "")
            if fname or lname:
                authors.append(f"{fname} {lname}".strip())
        article["authors"] = authors

        journal_info = article_data.get("Journal", {})
        article["journal"] = journal_info.get("Title")

        pub_date = journal_info.get("JournalIssue", {}).get("PubDate", {})
        year = pub_date.get("Year")
        month = pub_date.get("Month") or "01"
        day = pub_date.get("Day") or "01"

        if year:
            article["publication_date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            article["publication_date"] = None

        article["source"] = "pubmed"

        # Minimal required fields for ingestion
        if not article["pmid"] or not article["abstract"]:
            return None
        return article
    except Exception as e:
        print(f"⚠️ Skipped malformed entry: {e}")
        return None

def batch_fetch(pmids, start_index):
    total = len(pmids)
    processed, skipped = 0, 0

    with open(DATA_FILE, "a", encoding="utf-8") as outfile:
        for i in range(start_index, total, BATCH_SIZE):
            batch = pmids[i:i + BATCH_SIZE]
            try:
                print(f"📥 Fetching articles {i + 1} to {i + len(batch)}")
                handle = Entrez.efetch(db="pubmed", id=",".join(batch), rettype="xml", retmode="xml")
                records = Entrez.read(handle)

                for entry in records.get("PubmedArticle", []):
                    parsed = parse_pubmed_article(entry)
                    if parsed:
                        outfile.write(json.dumps(parsed) + "\n")
                        processed += 1
                    else:
                        skipped += 1

                save_progress(i + BATCH_SIZE)
                time.sleep(SLEEP_BETWEEN_CALLS)
            except Exception as e:
                print(f"❌ Error at batch {i}: {e}")
                time.sleep(5)
                continue

    print(f"\n✅ Done. Processed: {processed} | Skipped: {skipped}")

# === MAIN ===
if __name__ == "__main__":
    pmid_list = load_pmids()
    resume_from = load_progress()
    print(f"⏩ Resuming from index {resume_from} of {len(pmid_list)} PMIDs")
    batch_fetch(pmid_list, resume_from)
    print(f"✅ Fetch complete — Saved to: {DATA_FILE}")
