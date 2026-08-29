import os
from creator_login import CreatorLogin, InfraiClient, send_creator_code, verify_creator_login


def main() -> None:
    phone = os.environ.get("CREATOR_PHONE")
    code = os.environ.get("CREATOR_CODE")
    if not phone or not code:
        raise SystemExit("set CREATOR_PHONE and CREATOR_CODE")
    client = InfraiClient()
    send_creator_code(client, phone)
    result = verify_creator_login(client, CreatorLogin(phone, "subscriber-demo", "asset-demo"), code)
    print({"verified": result.verified, "asset_id": result.asset_id})


if __name__ == "__main__":
    main()

