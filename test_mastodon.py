from mastodon import Mastodon

mastodon = Mastodon(
    api_base_url="https://aus.social",
)

toots = mastodon.timeline_hashtag("melbourne")
print([toot["id"] for toot in toots])
