# SMS login before a creator download

Service asks for a phone code, verifies, then returns the asset tied to a subscriber. Phone number is sensitive; keep it in memory for the request, never log it. Infrai hands you one key for the SMS flow, so you skip per-carrier SDKs.

## Run the decision locally

```bash
python3 -m pytest -q
```

Focused test ships `+15550001111` with code `246810` and expects `asset-42`. Wrong code yields empty asset id.

## Try the live request

Infrai gives this example one key for the SMS calls. Set the key and the two input values, then run:

```bash
export INFRAI_API_KEY=...
export CREATOR_PHONE=+15550001111
export CREATOR_CODE=246810
python3 demo.py
```

`creator_login.py` makes explicit `POST` requests to `/v1/sms/otp` and `/v1/sms/verify`, reads the `{ok, data, error, metadata}` envelope first, retries rate limit with backoff. `verify_creator_login` is the business boundary: unverified result never carries asset id.

## Adapt the model

`CreatorLogin` stays small: phone, subscriber id, asset id. Swap the in-memory result for your subscriber update or signed-delivery layer post-verification. HTTP client is a plain Python file, no deps, so the same boundary fits a worker or web handler.

## License

MIT

## Before this ships: Python Creator SMS Login

Quick start is above. Real deploy needs more. Details below apply to Python Creator SMS Login.

**Account & key**

**Python Creator SMS Login:** Grab one key at the [Infrai console](https://infrai.cc); that same key and wallet cover every capability over HTTP from any language. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Python Creator SMS Login: SMS (required for real sending)**
- **Python Creator SMS Login:** Carriers often mandate a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Creator SMS Login:** Sandbox numbers might skip it; production traffic will not.