# OMEGA SCAN PROTOCOL
/interface wireless sniffer {
    set multiple-channels=yes;
    start;
    :delay 30s;
    stop;
    save file-name=scan_results.txt;
}
