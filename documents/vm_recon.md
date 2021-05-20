# Recon Ops
## [10.86.229.25](http://10.86.229.25)
### Nmap
```
> nmap -A 10.86.229.25
Starting Nmap 7.80 ( https://nmap.org ) at 2021-05-20 13:33 AEST
Nmap scan report for 10.86.229.25
Host is up (0.0060s latency).
Not shown: 989 filtered ports
PORT     STATE  SERVICE         VERSION
22/tcp   open   ssh             OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 38:32:62:63:95:cf:ba:3d:3f:01:79:72:7a:06:c0:9f (RSA)
|   256 e6:c8:e3:0d:e3:b1:32:6d:05:75:c5:7f:f6:0f:f7:42 (ECDSA)
|_  256 d8:ba:d1:86:9f:a5:13:aa:73:64:83:0a:5c:ed:52:82 (ED25519)
80/tcp   open   http            nginx 1.10.2
113/tcp  closed ident
443/tcp  open   ssl/http        nginx 1.10.2
|_http-server-header: nginx/1.10.2
|_http-title: Simple Student Templating Solutions
| ssl-cert: Subject: commonName=info2222g4.icu
| Subject Alternative Name: DNS:info2222g4.icu
| Not valid before: 2021-05-11T09:59:59
|_Not valid after:  2021-08-09T09:59:59
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
| tls-nextprotoneg: 
|_  http/1.1
2000/tcp open   cisco-sccp?
3306/tcp closed mysql
5060/tcp open   sip?
5432/tcp closed postgresql
8080/tcp closed http-proxy
8081/tcp closed blackice-icecap
8082/tcp closed blackice-alerts

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 248.21 seconds
```

### SSH
Tried to SSH into `root` and `rh` using default password `info2222`, not working.

`debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password,keyboard-interactive`

## [10.86.227.155](http://10.86.227.155)
### Nmap
```
> nmap -A 10.86.227.155
Starting Nmap 7.80 ( https://nmap.org ) at 2021-05-20 13:33 AEST
Nmap scan report for 10.86.227.155
Host is up (0.0029s latency).
Not shown: 993 filtered ports
PORT     STATE  SERVICE     VERSION
22/tcp   open   ssh         OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 f7:e4:05:16:c2:8f:61:a4:62:db:5c:de:7a:27:76:52 (RSA)
|   256 8e:cd:0b:98:11:70:cd:97:97:c2:fb:fd:ad:3b:ca:24 (ECDSA)
|_  256 c9:d1:ed:29:c7:89:15:03:02:6d:da:1b:3b:4c:cb:d9 (ED25519)
80/tcp   open   http        nginx 1.12.2
|_http-server-header: nginx/1.12.2
|_http-title: Did not follow redirect to https://10.86.227.155/
113/tcp  closed ident
443/tcp  open   ssl/http    nginx 1.12.2
|_http-server-header: nginx/1.12.2
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
| ssl-cert: Subject: commonName=www.dfqnb.top
| Subject Alternative Name: DNS:www.dfqnb.top, DNS:dfqnb.top
| Not valid before: 2021-05-12T00:00:00
|_Not valid after:  2022-05-12T23:59:59
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
| tls-nextprotoneg: 
|_  http/1.1
2000/tcp open   cisco-sccp?
5060/tcp open   sip?
8080/tcp closed http-proxy

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 196.24 seconds
```

### SSH
No password authentication :(

`root@10.86.227.155: Permission denied (publickey,gssapi-keyex,gssapi-with-mic,keyboard-interactive).`

## [10.86.225.99](http://10.86.225.99)
Server dead? Cannot establish SSH, HTTP/HTTPS connection.
### Nmap
```
> nmap -A -Pn 10.86.225.99
Starting Nmap 7.80 ( https://nmap.org ) at 2021-05-20 13:34 AEST
Nmap scan report for 10.86.225.99
Host is up (0.0021s latency).
Not shown: 997 filtered ports
PORT     STATE  SERVICE     VERSION
113/tcp  closed ident
2000/tcp open   cisco-sccp?
5060/tcp open   sip?

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 200.47 seconds
```
### SSH
Cannot connect.

## [10.86.226.123](http://10.86.226.123)
### Nmap
```
> nmap -A 10.86.226.123
Starting Nmap 7.80 ( https://nmap.org ) at 2021-05-20 13:34 AEST
Nmap scan report for 10.86.226.123
Host is up (0.019s latency).
Not shown: 989 filtered ports
PORT     STATE  SERVICE         VERSION
22/tcp   open   ssh             OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 db:b1:15:4f:9c:9e:21:15:3b:a1:1b:c4:a3:fa:05:7b (RSA)
|   256 87:f5:90:fa:02:a0:8d:17:1d:33:ac:f9:0d:7e:09:b7 (ECDSA)
|_  256 0c:6e:7b:cf:4d:ca:97:b6:fd:7a:36:84:04:5b:a3:e7 (ED25519)
80/tcp   open   http            CherryPy wsgiserver
|_http-server-header: Cheroot/8.5.2
|_http-title: Simple Student Templating Solutions
113/tcp  closed ident
443/tcp  closed https
2000/tcp open   cisco-sccp?
3306/tcp closed mysql
5060/tcp open   sip?
5432/tcp closed postgresql
8080/tcp closed http-proxy
8081/tcp closed blackice-icecap
8082/tcp closed blackice-alerts

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 195.96 seconds
```

### SSH
Tried to SSH into `root` and `rh` using default password `info2222`, not working.

`debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password,keyboard-interactive
`
