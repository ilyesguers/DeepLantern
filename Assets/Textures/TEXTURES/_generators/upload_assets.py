"""Upload the pack to Roblox via Open Cloud and write the returned ids into luau/AssetIds.luau.

UNTESTED against the live API (written from the public Assets API docs). Run with --dry-run first.
Env: ROBLOX_API_KEY (Assets read+write), ROBLOX_USER_ID or ROBLOX_GROUP_ID.
Note: uploads as Decal; for UI/ImageLabel the engine resolves decal ids to their image. If your
account/API returns an Image asset type, change ASSET_TYPE.
"""
import argparse
import json
import os
import re
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSET_TYPE = "Decal"
API = "https://apis.roblox.com/assets/v1"


def files_from_ids_module():
    src = open(os.path.join(ROOT, "luau", "AssetIds.luau")).read()
    return re.findall(r'\["([^"]+)"\] = "([^"]*)"', src)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="path prefix filter, e.g. ui/ or icons/")
    ap.add_argument("--delay", type=float, default=0.6, help="seconds between uploads (rate limits)")
    a = ap.parse_args()
    pairs = [(p, i) for p, i in files_from_ids_module() if not a.only or p.startswith(a.only)]
    todo = [p for p, i in pairs if not i]
    print(f"{len(pairs)} entries, {len(todo)} need upload")
    if a.dry_run:
        for p in todo[:20]:
            print("would upload", p)
        return
    import requests
    key = os.environ["ROBLOX_API_KEY"]
    creator = {"userId": os.environ["ROBLOX_USER_ID"]} if os.environ.get("ROBLOX_USER_ID") else {"groupId": os.environ["ROBLOX_GROUP_ID"]}
    ids_path = os.path.join(ROOT, "luau", "asset_ids.json")
    done = json.load(open(ids_path)) if os.path.exists(ids_path) else {}
    for p in todo:
        if p in done:
            continue
        fp = os.path.join(ROOT, p if not p.startswith("ui/") else p)
        if not os.path.exists(fp):
            print("skip (file not found)", p)
            continue
        req = {"assetType": ASSET_TYPE, "displayName": "DL_" + p.replace("/", "_")[:40], "description": "Deep Lantern texture pack",
               "creationContext": {"creator": creator}}
        with open(fp, "rb") as f:
            r = requests.post(f"{API}/assets", headers={"x-api-key": key},
                              files={"request": (None, json.dumps(req), "application/json"), "fileContent": (os.path.basename(fp), f, "image/png")})
        if r.status_code != 200:
            print("FAIL", p, r.status_code, r.text[:200])
            continue
        op = r.json()["path"]
        for _ in range(30):
            time.sleep(1)
            o = requests.get(f"https://apis.roblox.com/assets/v1/{op}", headers={"x-api-key": key}).json()
            if o.get("done"):
                aid = o.get("response", {}).get("assetId")
                if aid:
                    done[p] = f"rbxassetid://{aid}"
                    print("ok", p, aid)
                else:
                    print("moderated/failed", p, json.dumps(o)[:160])
                break
        json.dump(done, open(ids_path, "w"), indent=1)
        time.sleep(a.delay)
    # write ids back into AssetIds.luau
    src = open(os.path.join(ROOT, "luau", "AssetIds.luau")).read()
    for p, v in done.items():
        src = src.replace(f'["{p}"] = ""', f'["{p}"] = "{v}"')
    open(os.path.join(ROOT, "luau", "AssetIds.luau"), "w").write(src)
    print("AssetIds.luau updated:", len(done), "ids")


if __name__ == "__main__":
    sys.exit(main())
