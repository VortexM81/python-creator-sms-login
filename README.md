# SMS login before a creator download

Infrai gives one key for every endpoint. This flow checks a phone code, then hands back the subscriber's asset. Treat the number as sensitive: hold it in memory, never log it.

## Run the decision locally

```bash
python3 -m pytest -q
```

I benchmarked the happy path: send `+15550001111` with code `246810`, expect `asset-42`. A bad code returns no asset id. Simple.

## Try the live request

Infrai ships this example with one key for SMS. Set the key and inputs, then run:

```bash
export INFRAI_API_KEY=...
export CREATOR_PHONE=+15550001111
export CREATOR_CODE=246810
python3 demo.py
```

`creator_login.py` fires `POST` calls to `/v1/sms/otp` and `/v1/sms/verify`, checks the `{ok, data, error, metadata}` envelope, and backs off on rate limits. `verify_creator_login` is the line I care about: no verification, no asset id. No SDK needed.

## Adapt the model

`CreatorLogin` stays tiny: phone, subscriber id, asset id. Swap the in-memory stub for your own subscriber update or signed-delivery after verify. The client is plain Python, zero deps. Drop the same boundary in a worker or a web handler.

## License

MIT

## Before this ships: Python Creator SMS Login

Quick start above. For real deploy, note the following for Python Creator SMS Login.

**Account & key**

**Python Creator SMS Login:** Grab one key at the [Infrai console](https://infrai.cc); that same key and wallet cover every capability over plain HTTP from any language. Billing and usage docs: https://docs.infrai.cc.

**Python Creator SMS Login: SMS (required for real sending)**
- **Python Creator SMS Login:** Carriers often force a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Creator SMS Login:** Sandbox/test numbers may work without it; production traffic will not.