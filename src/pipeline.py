import argparse, asyncio
from .collectors.arxiv import collect_concurrently
from .storage.jsonl import write_jsonl

async def main(out_dir):
    # Separate query shards make the collector horizontally scalable.
    queries = ["cat:cs.AI", "cat:cs.LG", "cat:cs.CL", "cat:cs.CV", "cat:cs.MA"]
    papers = await collect_concurrently(queries, page_size=100)
    write_jsonl(papers, f"{out_dir}/research_papers.jsonl")
    print(f"wrote {len(papers)} research paper records")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    parser.add_argument("--out", default="data")
    args = parser.parse_args()
    asyncio.run(main(args.out))
