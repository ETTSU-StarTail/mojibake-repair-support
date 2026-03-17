#!/usr/bin/env python
"""
文字化け復旧支援ツール - テストスクリプト
"""


def test_byte_conversion():
    """バイト列変換＆復元テスト（UI不要）"""

    # テスト対象関数をコピー（main.pyから独立）
    def normalize_codec_name(codec_name: str) -> str:
        """Pythonの文字コード名に正規化"""
        if "SIG" in codec_name or "BOM" in codec_name:
            return "utf-8-sig"
        return codec_name.lower().replace(" ", "-")

    def get_available_codecs() -> list:
        """主要な文字コード一覧"""
        return [
            "utf-8",
            "utf-8-sig",
            "shift_jis",
            "cp932",
            "euc_jp",
            "iso2022_jp",
            "utf_16_le",
            "utf_16_be",
            "utf_32",
            "iso8859_1",
            "ascii",
        ]

    def decode_with_all_codecs(byte_data: bytes) -> list:
        """バイト列を各文字コードで復元"""
        results = []
        codecs_to_try = get_available_codecs()

        for codec in codecs_to_try:
            try:
                decoded = byte_data.decode(codec)
                results.append((codec, decoded))
            except (UnicodeDecodeError, LookupError):
                pass

        return results

    # テスト1: UTF-8でエンコード
    test_text = "こんにちは"
    utf8_bytes = test_text.encode('utf-8')

    print(f"Test1: '{test_text}' を UTF-8 でバイト列化")
    print(f"  UTF-8 バイト列: {utf8_bytes.hex()}")

    results = decode_with_all_codecs(utf8_bytes)
    print(f"  復元成功: {len(results)} 件")
    for codec, decoded in results[:3]:
        print(f"    {codec}: {decoded}")

    # テスト2: Shift_JISでエンコード
    sjis_bytes = test_text.encode('shift_jis')
    print(f"\nTest2: '{test_text}' を Shift_JIS でバイト列化")
    print(f"  Shift_JIS バイト列: {sjis_bytes.hex()}")

    results2 = decode_with_all_codecs(sjis_bytes)
    print(f"  復元成功: {len(results2)} 件")
    for codec, decoded in results2[:3]:
        print(f"    {codec}: {decoded}")

    print("\n✓ テスト完了")


if __name__ == "__main__":
    test_byte_conversion()
