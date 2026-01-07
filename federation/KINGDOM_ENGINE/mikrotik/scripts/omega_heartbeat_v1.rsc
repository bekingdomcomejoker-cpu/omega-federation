# HARDENED V1: OMEGA HEARTBEAT (RouterOS)
# Append-only hardware witness

:log info "OMEGA_V1: Heartbeat start"

:local sysname [/system identity get name]
:local uptime [/system resource get uptime]
:local cpuload [/system resource get cpu-load]
:local freemem [/system resource get free-memory]
:local totalmem [/system resource get total-memory]

:local memused ($totalmem - $freemem)
:local mempercent (($memused * 100) / $totalmem)

:local rxbytes 0
:local txbytes 0
:foreach i in=[/interface find] do={
    :if ([/interface get $i running]) do={
        :set rxbytes ($rxbytes + [/interface get $i rx-byte])
        :set txbytes ($txbytes + [/interface get $i tx-byte])
    }
}

:log info ("OMEGA|V1|sys=" . $sysname . \
"|uptime=" . $uptime . \
"|cpu=" . $cpuload . \
"|mem=" . $mempercent . \
"|rx=" . $rxbytes . \
"|tx=" . $txbytes)

:if ([:len [/file find name=\"kingdom_command.rsc\"]] > 0) do={
    :local cmd [/file get kingdom_command.rsc contents]
    :log info ("OMEGA|V1|CMD|" . $cmd)
    /file remove kingdom_command.rsc
}

:log info "OMEGA_V1: Heartbeat end"
