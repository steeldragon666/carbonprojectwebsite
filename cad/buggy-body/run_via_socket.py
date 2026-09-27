#!/usr/bin/env python3
"""Drive fusion_buggy_body.py through the Fusion360MCP socket add-in
(localhost:9876) instead of the Scripts dialog - one stage per execute_code
payload so the add-in's "small payloads, verify between stages" rule holds.

Run on the machine where Fusion is open (stdlib only):

    python run_via_socket.py

The module state (measured chassis, component handles) persists between
payloads because the script is imported once into Fusion's interpreter.
"""
import json
import os
import socket
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 9876
STAGES = [
    "stage_measure_chassis", "stage_create_component", "stage_cage", "stage_lattices",
    "stage_tub", "stage_hood_deck", "stage_spine_channel", "stage_fenders",
    "stage_seats_fittings", "stage_reference_wheels", "stage_generative_design_setup",
    "stage_finish",
]


def fz(cmd, params=None, timeout=300):
    s = socket.create_connection(("localhost", PORT), timeout=timeout)
    msg = {"type": cmd}
    if params is not None:
        msg["params"] = params
    s.sendall((json.dumps(msg) + "\n").encode())
    buf = b""
    while b"\n" not in buf:
        chunk = s.recv(65536)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf.decode().strip())


def code(snippet, tag):
    r = fz("execute_code", {"code": snippet})
    res = r.get("result", {}) or {}
    ok = r.get("status") == "success" and res.get("ok", True)
    print("[%s] ok=%s" % (tag, ok) + ("" if ok else "  ERR=%s hints=%s" % (res.get("error_message"), res.get("hints"))))
    if not ok:
        raise SystemExit("stage %s failed - see fusion_build.log next to the script" % tag)
    return res


def main():
    print("ping:", fz("ping"))
    t0 = time.time()
    here = HERE.replace("\\", "\\\\")
    code("import sys, importlib\n"
         "sys.path.insert(0, r'%s') if r'%s' not in sys.path else None\n"
         "import fusion_buggy_body as fb\n"
         "importlib.reload(fb)\n"
         "import adsk.core, adsk.fusion, time\n"
         "fb.C.app = adsk.core.Application.get(); fb.C.ui = fb.C.app.userInterface; fb.C.t0 = time.time()\n"
         "fb.C.design = adsk.fusion.Design.cast(fb.C.app.activeProduct)\n"
         "result = fb.C.app.activeDocument.name" % (here, here), "init")
    for st in STAGES:
        code("import fusion_buggy_body as fb\n"
             "fb.%s()\n"
             "result = 'failures=' + ','.join(f[0] for f in fb.C.failures)" % st, st)
        log = os.path.join(HERE, "fusion_build.log")
        if os.path.exists(log):
            with open(log) as fh:
                tail = [l.rstrip() for l in fh.readlines()[-3:]]
            for l in tail:
                if "FAILED" in l or "WARN" in l:
                    print("   ", l)
    rep = os.path.join(HERE, "fusion_report.json")
    if os.path.exists(rep):
        with open(rep) as fh:
            s = json.load(fh)["summary"]
        print(json.dumps(s, indent=2))
    print("done in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
