# Various bunq API scripts
I open source here some of my scripts, which I use to make my banking experience
 with bunq better. You're free to use them as well. However, I can't take any
 responsibility for what might happen if you use them.

## Pinsparen
Inspired by Michiel, I wrote a small library, which rounds the balances of my
accounts to either x.00 or x.50 whenever any balance of any account changes.
This helps me to save some cents here and there whenever I e.g. pay by card in
the supermarket.

### How to use it:
Simply add your information like e.g. API key in the pinsparen.py file and run
that file (with Python3.6). It will automatically check the balances of your
accounts whenever
any of the balances changes and transfer the 'excess' cents to your savings.
