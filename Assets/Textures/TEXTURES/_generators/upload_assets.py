"""Safely upload texture assets through Roblox Open Cloud.

This script has not been validated against a live Roblox account. Start with --dry-run.
Required environment: ROBLOX_API_KEY and exactly one of ROBLOX_USER_ID / ROBLOX_GROUP_ID.
Progress is saved to luau/asset_ids.json after each completed upload. AssetIds.luau is
updated atomically so an interrupted run does not leave a partially written source file.
"""
import argparse
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LUAU_DIR = ROOT / "luau"
IDS_MODULE = LUAU_DIR / "AssetIds.luau"
PROGRESS_FILE = LUAU_DIR / "asset_ids.json"
ASSET_TYPE = "Decal"
API = "https://apis.roblox.com/assets/v1"
REQUEST_TIMEOUT = (10, 60)
POLL_TIMEOUT = (10, 30)
MAX_POLL_ATTEMPTS = 60
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def files_from_ids_module():
    if not IDS_MODULE.is_file():
        raise RuntimeError(f"Asset ID module not found: {IDS_MODULE}")
    pairs = re.findall(r'\["([^"]+)"\]\s*=\s*"([^"]*)"', IDS_MODULE.read_text(encoding="utf-8"))
    if not pairs:
        raise RuntimeError(f"No asset entries found in {IDS_MODULE}")
    return pairs


def atomic_write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def save_progress(done):
    atomic_write(PROGRESS_FILE, json.dumps(done, indent=2, sort_keys=True) + "\n")


def read_progress():
    if not PROGRESS_FILE.exists():
        return {}
    try:
        value = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read progress file {PROGRESS_FILE}: {exc}") from exc
    if not isinstance(value, dict) or any(
        not isinstance(k, str) or not isinstance(v, str)
        or not re.fullmatch(r"rbxassetid://\d+", v)
        for k, v in value.items()
    ):
        raise RuntimeError(f"Invalid entries in {PROGRESS_FILE}; back it up and correct it before uploading")
    return value


def request_with_retries(session, method, url, *, attempts=4, **kwargs):
    timeout = kwargs.pop("timeout", REQUEST_TIMEOUT)
    last_error = None
    for attempt in range(attempts):
        try:
            response = session.request(method, url, timeout=timeout, **kwargs)
            if response.status_code not in RETRYABLE_STATUS or attempt == attempts - 1:
                return response
            last_error = RuntimeError(f"HTTP {response.status_code}: {response.text[:200]}")
            retry_after = response.headers.get("Retry-After", "")
            try:
                wait = min(max(float(retry_after), 1), 30)
            except (TypeError, ValueError):
                wait = min(2 ** attempt, 8)
        except Exception as exc:
            import requests
            if not isinstance(exc, requests.RequestException) or attempt == attempts - 1:
                raise
            last_error = exc
            wait = min(2 ** attempt, 8)
        time.sleep(wait)
    raise RuntimeError(f"Request failed after retries: {last_error}")


def resolve_asset_path(relative_path):
    candidate = (ROOT / relative_path).resolve()
    if candidate == ROOT or ROOT not in candidate.parents:
        raise RuntimeError(f"Unsafe path outside texture root: {relative_path}")
    if not candidate.is_file():
        raise FileNotFoundError(f"Asset file does not exist: {relative_path}")
    if candidate.suffix.lower() != ".png":
        raise RuntimeError(f"Only PNG files are supported by this uploader: {relative_path}")
    return candidate


def write_ids_module(done):
    src = IDS_MODULE.read_text(encoding="utf-8")
    for path, asset_id in done.items():
        escaped_path = re.escape(path)
        pattern = re.compile(r'(\["' + escaped_path + r'"\]\s*=\s*")[^"]*(")')
        src, count = pattern.subn(lambda m: m.group(1) + asset_id + m.group(2), src)
        if count > 1:
            raise RuntimeError(f"Duplicate AssetIds.luau key: {path}")
    atomic_write(IDS_MODULE, src)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="validate files without network calls")
    parser.add_argument("--only", help="path prefix filter, e.g. ui/ or icons/")
    parser.add_argument("--delay", type=float, default=0.6, help="seconds between uploads")
    parser.add_argument("--poll-attempts", type=int, default=MAX_POLL_ATTEMPTS, help="maximum status checks per upload")
    args = parser.parse_args()
    if args.delay < 0:
        parser.error("--delay must be zero or greater")
    if args.poll_attempts < 1:
        parser.error("--poll-attempts must be at least 1")

    pairs = files_from_ids_module()
    if args.only:
        pairs = [(path, asset_id) for path, asset_id in pairs if path.startswith(args.only)]
    if not pairs:
        raise RuntimeError("No asset entries match the requested filter")
    if len({path for path, _ in pairs}) != len(pairs):
        raise RuntimeError("Duplicate paths found in AssetIds.luau")

    done = read_progress()
    todo = [(path, asset_id) for path, asset_id in pairs if not asset_id and path not in done]
    invalid = [(path, value) for path, value in pairs if value and not re.fullmatch(r"rbxassetid://\d+", value)]
    if invalid:
        raise RuntimeError(f"Invalid existing asset ID for {invalid[0][0]}")

    files, missing = {}, []
    for path, _ in todo:
        try:
            files[path] = resolve_asset_path(path)
        except (RuntimeError, OSError) as exc:
            missing.append(str(exc))
    print(f"{len(pairs)} entries selected; {len(todo)} pending; {len(done)} saved progress entries")
    if missing:
        print("Preflight errors:")
        for error in missing:
            print(" -", error)
        raise RuntimeError("Preflight failed; no uploads were attempted")
    if args.dry_run:
        for path in list(files)[:20]:
            print("would upload", path)
        if len(files) > 20:
            print(f"... and {len(files) - 20} more")
        print("Dry run complete: no network calls or file changes made.")
        return 0
    if not todo:
        print("No pending assets.")
        return 0

    key = os.environ.get("ROBLOX_API_KEY", "").strip()
    user_id = os.environ.get("ROBLOX_USER_ID", "").strip()
    group_id = os.environ.get("ROBLOX_GROUP_ID", "").strip()
    if not key:
        raise RuntimeError("ROBLOX_API_KEY is required")
    if bool(user_id) == bool(group_id):
        raise RuntimeError("Set exactly one of ROBLOX_USER_ID or ROBLOX_GROUP_ID")
    creator = {"userId": user_id} if user_id else {"groupId": group_id}

    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("The requests package is required; install it with: python -m pip install requests") from exc
    session = requests.Session()
    session.headers.update({"x-api-key": key})
    failed = []

    for path, _ in todo:
        if path in done:
            continue
        request_body = {
            "assetType": ASSET_TYPE,
            "displayName": "DL_" + path.replace("/", "_")[:40],
            "description": "Deep Lantern texture pack",
            "creationContext": {"creator": creator},
        }
        try:
            with files[path].open("rb") as image_file:
                response = request_with_retries(
                    session, "POST", f"{API}/assets",
                    files={
                        "request": (None, json.dumps(request_body), "application/json"),
                        "fileContent": (files[path].name, image_file, "image/png"),
                    },
                )
            if response.status_code not in (200, 201, 202):
                raise RuntimeError(f"upload HTTP {response.status_code}: {response.text[:300]}")
            try:
                operation = response.json().get("path")
            except (ValueError, AttributeError) as exc:
                raise RuntimeError("upload response was not valid JSON") from exc
            if not isinstance(operation, str) or not operation:
                raise RuntimeError("upload response did not include an operation path")

            completed = False
            for _ in range(args.poll_attempts):
                time.sleep(1)
                status = request_with_retries(session, "GET", f"{API}/{operation}", timeout=POLL_TIMEOUT)
                if status.status_code != 200:
                    raise RuntimeError(f"status HTTP {status.status_code}: {status.text[:300]}")
                try:
                    state = status.json()
                except ValueError as exc:
                    raise RuntimeError("status response was not valid JSON") from exc
                if state.get("done") is True:
                    asset_id = (state.get("response") or {}).get("assetId")
                    if asset_id is None or not str(asset_id).isdigit():
                        raise RuntimeError(f"operation completed without a valid assetId: {json.dumps(state)[:300]}")
                    done[path] = f"rbxassetid://{asset_id}"
                    save_progress(done)
                    write_ids_module(done)
                    print(f"ok {path}: {asset_id}")
                    completed = True
                    break
                if state.get("error"):
                    raise RuntimeError(f"Roblox operation error: {json.dumps(state['error'])[:300]}")
            if not completed:
                raise RuntimeError(f"operation did not finish after {args.poll_attempts} status checks; rerun to continue")
        except Exception as exc:
            failed.append((path, str(exc)))
            print(f"FAIL {path}: {exc}", file=sys.stderr)
        time.sleep(args.delay)

    write_ids_module(done)
    print(f"Saved {len(done)} asset IDs to {PROGRESS_FILE} and {IDS_MODULE}")
    if failed:
        print(f"{len(failed)} upload(s) failed; rerun after fixing the cause.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
