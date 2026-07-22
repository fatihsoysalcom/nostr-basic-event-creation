import time
import json
import hashlib
import secp256k1

def create_nostr_event(private_key_hex, content, kind=1):
    """Creates a basic Nostr event (a text note).

    Args:
        private_key_hex (str): The user's private key in hexadecimal format.
        content (str): The message content of the event.
        kind (int): The kind of the event (default is 1 for text notes).

    Returns:
        dict: The Nostr event object.
    """
    # Derive public key from private key
    sk = secp256k1.PrivateKey(bytes.fromhex(private_key_hex))
    pk = sk.pubkey
    public_key_hex = pk.serialize().hex()

    # Current timestamp in seconds
    created_at = int(time.time())

    # Construct the event payload (without signature)
    event_payload = [
        0,  # Version (always 0 for Nostr)
        public_key_hex,
        created_at,
        kind,
        [], # Tags (empty for this basic example)
        content
    ]

    # Serialize the event payload and hash it to get the event ID
    event_id = hashlib.sha256(json.dumps(event_payload, separators=(',', ':')).encode('utf-8')).hexdigest()

    # Sign the event ID with the private key
    signature = sk.schnorr_sign(bytes.fromhex(event_id)).hex()

    # Assemble the final event object
    event = {
        "id": event_id,
        "pubkey": public_key_hex,
        "created_at": created_at,
        "kind": kind,
        "tags": [],
        "content": content,
        "sig": signature
    }

    return event

if __name__ == "__main__":
    # --- IMPORTANT ---
    # Replace with your actual private key. NEVER share your private key.
    # For testing, you can generate one using `openssl rand -hex 32`
    # or a dedicated Nostr key generator.
    TEST_PRIVATE_KEY = "YOUR_32_BYTE_HEX_PRIVATE_KEY"

    if TEST_PRIVATE_KEY == "YOUR_32_BYTE_HEX_PRIVATE_KEY":
        print("Please replace 'YOUR_32_BYTE_HEX_PRIVATE_KEY' with your actual private key.")
    else:
        message_content = "Hello Nostr from my custom desktop client! #Nostr #DevTo"
        nostr_event = create_nostr_event(TEST_PRIVATE_KEY, message_content)

        print("Generated Nostr Event:")
        print(json.dumps(nostr_event, indent=2))

        # In a real client, you would now send this event to a Nostr relay.
        # This example only demonstrates event creation and signing.
