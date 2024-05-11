from mastodon import Mastodon

mastodon = Mastodon(
    api_base_url="https://aus.social",
    access_token="OTPi29TLCpygo_S5XC9Tpb6GbcxGj9qeSCsRrMVBask",
)

toots = mastodon.timeline_hashtag("melbourne")
print(len(toots))
