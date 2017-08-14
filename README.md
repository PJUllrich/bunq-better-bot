# Better Bunq Bot

This is still very much work-in-progress.
Check back in here in a bit, please!

## Security


### Key Derivation Function (KDF)
Most popular KDFs are `PBKDF2`, `bcrypt`, and `scrypt`, whereas `scrypt`
 is considered the 'most secure' one again brute-force attacks (add source).
I decided on using `scrypt` for this project for the following reason:
1. `PBKDF2` is the most common and scrutinized one. However, since its
algorithm is neither computational nor memory costly, brute-forcing can
be done on it with relatively low cost (see source)
2. `Bcrypt` is more computational expensive due to its design, however the
hashed key in the output is 'only' **184bit** long and can therefore not be
used for an e.g. `AES-256` encryption. I could have used a `HKDF` function
to widen the key to 256bit, but this would have been extra computational
expensive and the advantages of extra scrutiny this algorithm has
experienced due to its age did for me now outweigh the advantages which
`scrypt` offered.
3. `Scrypt` is the latest popular KDF and is both computational
expensive and 'very' memory consuming. Brute-forcing a password hashed
with `scrypt` entails the highest utility costs, which makes it more
secure than the other KDFs. The implementation of `scrypt` which is used
in this project is included in `Pycryptodomex`, which is the same
library which is used in the bunq Python SDK (add source). `Scrypt`
can return keys of 256bit length (or even longer if requested), which
means that the hashes produced by `scrypt` can be used in e.g. an
`AES-256` encryption.

## Decisions
* Chat_ID and API Key are always sent in the clear to the backend with
trust in HTTPS to protect this data from attackers.
* Password is hashed once on client side before being sent to backend.
Rationale: I don't want to see users password in the clear anywhere on
the backend. Somehow it feels like an invasion in their privacy. A hash
is more anonymous than a password.
* All passwords and salts are handled and stored as **bytes**.
Rationale: All functions that use such variables require bytes as input,
thus instead of en- and decoding str to bytes all the time, such
variables will simply stay bytes.

## Environment Variables
**Backend**

**Bot**
* BUNQ_BOT_URL = e.g. `https://www.example.com`
* BUNQ_BOT_URL_PATH = e.g. `/telegram-bot`
* BUNQ_BOT_TOKEN = e.g. `123456789abcdefgehijklmnop` (from BotFather)
* BUNQ_BOT_BACKEND_URL = e.g. `http://localhost:5000`





