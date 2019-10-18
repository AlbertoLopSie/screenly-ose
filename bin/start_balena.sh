#!/bin/bash
APP_REPO="AlbertoLopSie/screenly-ose"
APP_NAME="screenly"
APP_FOLDER="screenly"
APP_DISPLAYNAME="Screenly OSE"

run_setup () {
    mkdir -p \
        /data/.config \
        /data/.config/uzbl \
        /data/.$APP_FOLDER \
        /data/$APP_FOLDER \
        /data/$APP_FOLDER_assets

    cp -n /tmp/$APP_FOLDER/ansible/roles/$APP_FOLDER/files/$APP_NAME.conf /data/.$APP_FOLDER/$APP_NAME.conf
    cp -n /tmp/$APP_FOLDER/ansible/roles/$APP_FOLDER/files/default_assets.yml /data/.$APP_FOLDER/default_assets.yml
    cp -n /tmp/$APP_FOLDER/ansible/roles/$APP_FOLDER/files/$APP_FOLDER.db /data/.$APP_FOLDER/$APP_NAME.db
    cp -n /tmp/$APP_FOLDER/ansible/roles/$APP_FOLDER/files/uzbl-config /data/.config/uzbl/config-$APP_NAME

    cp -rf /tmp/$APP_FOLDER/* /data/$APP_FOLDER/

    if [ -n "${OVERWRITE_CONFIG}" ]; then
        echo "Requested to overwrite Screenly config file."
        cp /data/$APP_FOLDER/ansible/roles/$APP_FOLDER/files/$APP_NAME.conf "/data/.$APP_FOLDER/$APP_NAME.conf"
    fi

    # Set management page's user and password from environment variables,
    # but only if both of them are provided. Can have empty values provided.
    if [ -n "${MANAGEMENT_USER+x}" ] && [ -n "${MANAGEMENT_PASSWORD+x}" ]; then
        sed -i -e "s/^user=.*/user=${MANAGEMENT_USER}/" -e "s/^password=.*/password=${MANAGEMENT_PASSWORD}/" /data/.$APP_FOLDER/$APP_NAME.conf
    fi

    /usr/bin/python /data/$APP_FOLDER/bin/migrate.py
}

run_viewer () {
    # By default docker gives us 64MB of shared memory size but to display heavy
    # pages we need more.
    umount /dev/shm && mount -t tmpfs shm /dev/shm

    while true; do

        /usr/bin/X 0<&- &>/dev/null &
        /usr/bin/matchbox-window-manager -use_titlebar no -use_cursor no 0<&- &>/dev/null &

        error=$(/usr/bin/xset s off 2>&1 | grep -c "unable to open display")
            if [[ "$error" -eq 0 ]]; then
            break
        fi

        echo "Still continue..."
        sleep 1
    done

    /usr/bin/xset -dpms
    /usr/bin/xset s noblank

    while true; do

        error=$(curl 127.0.0.1:8080 2>&1 | grep -c "Failed to connect")
            if [[ "$error" -eq 0 ]]; then
            break
        fi

        echo "Still continue..."
        sleep 1
    done

    cd /data/$APP_FOLDER
    /usr/bin/python viewer.py
}

run_server () {
    service nginx start

    export RESIN_UUID=${RESIN_DEVICE_UUID}

    cd /data/$APP_FOLDER
    /usr/bin/python server.py
}

run_websocket () {
    cd /data/$APP_FOLDER
    /usr/bin/python websocket_server_layer.py
}

run_celery () {
    cd /data/$APP_FOLDER
    celery worker -A server.celery -B -n worker@$APP_NAME --loglevel=info --schedule /tmp/celerybeat-schedule
}

if [[ "$SCREENLYSERVICE" = "server" ]]; then
    run_setup
    run_server
fi

if [[ "$SCREENLYSERVICE" = "viewer" ]]; then
    run_viewer
fi

if [[ "$SCREENLYSERVICE" = "websocket" ]]; then
    run_websocket
fi

if [[ "$SCREENLYSERVICE" = "celery" ]]; then
    run_celery
fi