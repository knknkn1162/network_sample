
+ use certbot

## how to generate certification file

```sh
DOMAIN="your.domain"; docker run -it --rm -v "./etc:/etc/letsencrypt" certbot/certbot certonly --manual --preferred-challenges dns-01 --agree-tos -m knknkn1162@gmail.com -d "*.${DOMAIN}"
```