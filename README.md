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
that file (with Python3.6). It will automatically check the balances of your
accounts whenever any of the balances changes and transfer the 'excess' cents to
 your savings.

## Your own Server
In order to use e.g. Pinsparen you will need your own server with an own URL and
 an HTTPS certificate for that URL. I created a small overview of
 what you need to do, if you don't have any or only some of aforementioned
 required things.

### What you need is:
1. Your own URL to which bunq can send the Callback notifications
2. A HTTPS certificate for that URL
3. A static IP (look out for this when renting a server, should be included)
4. An API Key (you can get that from the App)

### How to get these things:
**Disclaimer**: I'm not getting paid for giving any of the product or
service recommendations in the following. It's simply what I use and am
satisfied with.

1. Rent your own server! I rent my VPS (Virtual Private Server) with CentOS 7
for ~2.50E/month at [Host1Plus](https://www.host1plus.com/)
2. Purchase your own URL! I did that at GoDaddy.com for about 10Euro/year
3. Point that URL from GoDaddy to the IP of your Server ( [Host1Plus Tutorial](https://support.host1plus.com/index.php?/Knowledgebase/Article/View/1258/0/how-to-point-my-domain-to-your-dns-manager) )

From here on all traffic to my URL is rerouted to my VPS, now to set that VPS up:

1. Install [Nginx](https://www.nginx.com/resources/wiki/) and set up a Server
Block ( [see Tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-on-centos-7) )
for your URL
2. In that Server Block create a proxy_pass ( [see Tutorial](https://gist.github.com/soheilhy/8b94347ff8336d971ad0) ) for a sub-domain (e.g
. http://www.yoururl.com/callbacks) to the Port you specify in the Pinsparen.py
script (I set it to 8500, all ports below 1024 need special permission, so use
a 'high' port)
3. Set up a HTTPS certificate for your url ( [see Tutorial](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-centos-7) )
4. Pin this HTTPS certificate with the bunq API ( [see Docs](https://doc.bunq.com/api/1/page/callbacks) (below))
5. Don't forget to restart nginx with e.g. `nginx -s stop` and then start it
with `nginx`

Now, all traffic to the sub-domain you specified will be rerouted to the Port
you specified in the proxy_pass config. If you set the pinsparen.py script to
the same port and start it with `python3.6 pinsparen.py` it will be able to
receive and react to callbacks from the bunq API.

*Hint*: If you want to let the `pinsparen.py` script in the background
and also when you log out from your server, use `nohup` to 'disown' the
script process from your shell session, otherwise the server will kill
that process whenever you log out. This is the command you need:
`nohup python3.6 pinsparen.py &`
