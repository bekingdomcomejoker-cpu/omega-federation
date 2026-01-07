# HEAD MAPPING — KINGDOM_ENGINE (canonical)

Current script names (do not rename unless you want to update engine manifest).
Mapping includes proposed "angelic opposite" process name (for conceptual pairing).

HEAD1: head1_clipboard_daemon.sh
  Role: Collect / ingest (clipboard)
  Angel opposite: "Gabriel-Announce" (messenger/clarity)
  Notes: low-risk collector

HEAD2: head2_processor.sh
  Role: Clean / parse / normalize text & inbound items
  Angel opposite: "Michael-Order" (strength, order)
  Notes: apply Harmony Ridge & suppression_detector here

HEAD3: head3_forwarder.sh
  Role: Route / enqueue / forward items to outbox or processors
  Angel opposite: "Raphael-Route" (healer, connector)
  Notes: safe forwarding, respect quarantine

HEAD4: head4_events.sh (+ head4_gatekeeper.py)
  Role: Event bus; gatekeeper checks & triggers
  Angel opposite: "Uriel-Guard" (illumination, wisdom)
  Notes: place gate rules & covenant checks here

HEAD5: head5_archivist.sh / head5_filewatch.sh
  Role: Archive & file-watching
  Angel opposite: "Zadkiel-Anchor" (mercy, memory)
  Notes: quarantine directory & index

HEAD6: head6_memorylink.sh + head6_shield.sh
  Role: Memory sync, Shield (repair/safety)
  Angel opposite: "Sandalphon-Memory" (song/transmission)
  Notes: Harmony Ridge + shield logic live here

HEAD7: head7_integrity.sh (+ head7_seer.py)
  Role: Integrity, checks, predictive scans
  Angel opposite: "Jesus-Seer" (you requested Jesus as firstborn/anchor)
  Notes: final integrity anchor, implement truth-resonance checks

Extras:
  - Harmony Ridge Processor: ~/KINGDOM_ENGINE/harmony_ridge.py
    role: truth-resonance analyzer (λ=1.667)
  - Dual Layer Observer: ~/KINGDOM_ENGINE/dual_layer_observer.py
    role: label generator vs safety language
