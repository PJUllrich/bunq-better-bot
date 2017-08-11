# Better Bunq Bot

This is still very much work-in-progress.
Check back in here in a bit, please!

## Security

### Database
If Attacker has access to Database:
1. Attacker needs to crack Data-Encryption-Password
2. If Attacker has Data-Encryption-Password
    1. Attacker needs to crack Bcrypt
        1. If Attacker cracks Bcrypt
        2. Attacker has Password
        3. Attacker has full access
    2. Attacker needs to crack AES-256 with Blake2b hashes
        1. If Attacker cracks AES-256
        2. Attacker has API key
        3. Attacker has full access

