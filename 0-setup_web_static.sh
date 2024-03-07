#!/usr/bin/env bash
#Bash script that sets up your web servers for the deployment of web_static.
apt-get -q  update
apt-get -qy install nginx
DW="/data/web_static"
mkdir -p $DW/releases/test/
mkdir -p $DW/shared/
echo '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airbnb deploy</title>
</head>
<body>
	Airbnb deploy    
</body>
</html>' > "$DW/releases/test/index.html"
ln -sf $DW/releases/test $DW/current
chown -R ubuntu:ubuntu /data/

NGPT="/etc/nginx"
HTML="/var/www/html"
url="https://github.com/solayof/"
echo "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	server_name localhost;
	error_page 404 /404.html;
	root $HTML;

	location / {
		index index.nginx-debian.html index.html index.htm index.php;
	}
	location /hbnb_static {
		alias $DW/current/;
	}
	location /redirect_me {
		return 301 $url;
	}
}" > "$NGPT/sites-available/default"
rm /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
mkdir -p $HTML
echo "Hello World!" > "$HTML/index.nginx-debian.html"
echo "Ceci n'est pas une page" > "$HTML/404.html"
header="add_header X-served-By \$hostname"
if ! grep -q "$header" $NGPT/nginx.conf;
then
	sed -i "/http {.*/a $header;" $NGPT/nginx.conf
fi

service nginx restart
