import os
import time
import json
import urllib.request
import urllib.error

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

DEVICE_ID = os.getenv("BRIDGE_DEVICE_ID")
DEVICE_NAME = os.getenv("BRIDGE_DEVICE_NAME")

PENDAR_ID = "68aa8b3c-8617-45e1-b7c5-e07759baa97f"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase configuration is missing.")

if not DEVICE_ID or not DEVICE_NAME:
    raise RuntimeError("BRIDGE_DEVICE_ID or BRIDGE_DEVICE_NAME is missing.")


def request(method, path, data=None, extra_headers=None):
    url = SUPABASE_URL.rstrip("/") + path

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    if extra_headers:
        headers.update(extra_headers)

    body = None

    if data is not None:
        body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode("utf-8")

        if not raw:
            return None

        return json.loads(raw)


def heartbeat():
    from datetime import datetime, timezone

    data = {
        "device_id": DEVICE_ID,
        "device_name": DEVICE_NAME,
        "status": "online",
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }

    return request(
        "POST",
        "/rest/v1/bridge_devices?on_conflict=device_id",
        data,
        extra_headers={
            "Prefer": "resolution=merge-duplicates,return=minimal"
        },
    )


def get_devices():
    return request(
        "GET",
        "/rest/v1/bridge_devices?select=device_id,device_name,last_seen,status"
    )


def clear():
    os.system("clear")


def check_status():
    devices = get_devices()

    first_found = False
    second_found = False

    for device in devices:
        if device["device_id"] == DEVICE_ID:
            first_found = True

        if device["device_id"] == PENDAR_ID:
            second_found = True

    problems = []

    if not first_found:
        problems.append("دستگاه اول پیدا نشد")

    if not second_found:
        problems.append("دستگاه دوم پیدا نشد")

    clear()

    print("=" * 55)
    print("                 PROJECT BRIDGE")
    print("=" * 55)
    print()

    print("حل شده ها:")

    if not problems:
        print("هیچ مشکلی نیست، بین دستگاه ها هیچ مشکلی نیست")
    else:
        if first_found:
            print("دستگاه اول پیدا شد")

        if second_found:
            print("دستگاه دوم پیدا شد")

    print()
    print("مشکل ها:")

    if problems:
        for problem in problems:
            print(problem)
    else:
        print("هیچ مشکلی وجود ندارد")

    print()
    print("دستگاه فعلی:", DEVICE_NAME)
    print("وضعیت اتصال: آنلاین")

    print()
    print("=" * 55)


def main():
    while True:
        try:
            heartbeat()
            check_status()

        except urllib.error.URLError:
            clear()

            print("=" * 55)
            print("                 PROJECT BRIDGE")
            print("=" * 55)
            print()

            print("حل شده ها:")
            print("اتصال محلی دستگاه برقرار است")

            print()
            print("مشکل ها:")
            print("پیام ها ارسال نمیشوند")
            print("اتصال به Supabase برقرار نشد")

            print()
            print("=" * 55)

        except Exception as error:
            clear()

            print("=" * 55)
            print("                 PROJECT BRIDGE")
            print("=" * 55)
            print()

            print("حل شده ها:")
            print("هیچ مشکلی تأیید نشده")

            print()
            print("مشکل ها:")
            print("کد ایراد دارد")

            print()
            print("ERROR:", error)

            print()
            print("=" * 55)

        time.sleep(5)


if __name__ == "__main__":
    main()
