#!/bin/bash
APP_REPO="AlbertoLopSie/screenly-ose"
bash <(curl -H 'Cache-Control: no-cache' -sL --proto '=https' https://raw.githubusercontent.com/$APP_REPO/master/bin/install.sh)
