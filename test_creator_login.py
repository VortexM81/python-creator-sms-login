from creator_login import CreatorLogin, LoginResult, verify_creator_login


class FakeClient:
    def verify_otp(self, phone, code):
        return {"verified": phone == "+15550001111" and code == "246810"}


def test_verified_code_unlocks_asset():
    login = CreatorLogin("+15550001111", "subscriber-7", "asset-42")
    assert verify_creator_login(FakeClient(), login, "246810") == LoginResult(True, "subscriber-7", "asset-42")


def test_wrong_code_keeps_asset_private():
    login = CreatorLogin("+15550001111", "subscriber-7", "asset-42")
    result = verify_creator_login(FakeClient(), login, "000000")
    assert result.verified is False
    assert result.asset_id == ""

