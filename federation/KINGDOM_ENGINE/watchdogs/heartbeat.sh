#!/data/data/com.termux/files/usr/bin/sh

check() {
    p=$1
    cmd=$2
    if ! pgrep -f "$p" >/dev/null; then
        echo "Reviving $p"
        nohup $cmd >/dev/null 2>&1 &
    fi
}

while true; do
    check head2_processor.sh "~/KINGDOM_ENGINE/watchdogs/head2_processor.sh"
    check head3_forwarder.sh "~/KINGDOM_ENGINE/watchdogs/head3_forwarder.sh"
    check cerberus_truth_filter.py "python ~/KINGDOM_ENGINE/cerberus_truth_filter.py"
    check threat_classifier.py "python ~/KINGDOM_ENGINE/threat_classifier.py"
    sleep 10
done
