# VM Security Measures

## SSH

Configuration adapted from: [OpenSSH Configuration - MDN](https://infosec.mozilla.org/guidelines/openssh)

* Disabled password authentication (Key authentication only)
    - `PasswordAuthentication no`
    - `ChallengeResponseAuthentication no`
* Disabled root user login using SSH
    - `PermitRootLogin No`
* Verbose logging to log all SSH login
    - `LogLevel VERBOSE`

## Git Deploy
An RSA key is generated for the user `www-data` on the VM, the public key is then placed into the Github repository deploy key section with only read access so the VM have read access to the repository.

`ssh-keygen -b 4096`
```
The key fingerprint is:
SHA256:qgvYijkKGc8zfrp9/4oK2VbZjmuXVgWprLszemjg0Jc rh@ip-10-86-229-241.ap-southeast-2.compute.internal
The key's randomart image is:
+---[RSA 4096]----+
|           .     |
|          o      |
|       . . .     |
|       oo   .    |
|..   .o.S  .     |
|.BooE..+  .      |
|+oXoo.o..o       |
|++.B+.Bo+        |
|*.+=*B+Boo.      |
+----[SHA256]-----+
```

## HTTPS
Certbot is used to obtain a certificate from Let's Encrypt. The command used is `sudo certbot certonly --manual --preferred-challenges dns -d jerry.voyager.my`

## Nginx
* When a user visits via HTTP (Port 80), nginx will respond with 301 Moved to user to redirect user to the HTTPS version of the website. This is achieved by adding `return 301 https://$host$request_uri;` to the nginx config located at `/etc/nginx/nginx.conf` for the server listening at port 80.

Nginx acts as a reverse proxy to the bottle server. On the server listening on port 443, this configuration is added to make nginx a proxy between the bottle server and the client. Nginx currently act as a HTTP request proxy but this will be changed once uWsgi has been successfully deployed.

```
location / {
    proxy_pass http://localhost:8080;
}
```

The Let's Encrypt certificate is installed by specifying this 2 lines in the configuration file.
```
    ssl_certificate "/etc/letsencrypt/live/jerry.voyager.my/fullchain.pem";
    ssl_certificate_key "/etc/letsencrypt/live/jerry.voyager.my/privkey.pem";
```

Some of the server configuration were included from [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) where the nginx version is 1.16.1 and OpenSSL version is 1.1.1g, using the Intermediate configuration. [Config](https://ssl-config.mozilla.org/#server=nginx&version=1.16.1&config=intermediate&openssl=1.1.1g&guideline=5.6)

## Code deployment
A new normal user, `www-data` is created for this purpose. `useradd www-data`

The code base is restricted to this user by executing `chmod o-rwx info2222_M12B1`

A cron job is created to automatically pull the latest commit from the master branch every hour. `00 * * * * cd /home/www-data/info2222_M12B1; git pull &>> "/home/www-data/logs/git_pull.log"`. Underlying changes to the python code will still requires restart but any page added or removed will be available automatically.

`/etc/systemd/system/jerry.service`
```
[Unit]
Description=Bottle Python Server for Jerry
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/home/www-data/info2222_M12B1/code/
ExecStart=/usr/bin/python3 run.py
Restart=on-failure
RestartSec=10s
KillMode=process

[Install]
WantedBy=multi-user.target
```
Enable auto startup of service by systemd: `sudo systemctl enable jerry`

Nginx will be automatically started by default.

## uWsgi
