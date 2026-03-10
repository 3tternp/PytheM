#!/usr/bin/env python3
# coding=UTF-8

# Copyright (c) 2016 Angelo Moura
#
# This file is part of the program PytheM
#
# PytheM is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import argparse
import io
import json
import os
import secrets
import sys
import threading
import time
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from modules.utils import banner, color

version = "0.6.0"


def _require_root():
    geteuid = getattr(os, "geteuid", None)
    if callable(geteuid) and geteuid() != 0:
        sys.exit("[-] Only for roots kido! ")


class _JobStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._jobs = {}

    def create(self, kind, payload):
        job_id = secrets.token_urlsafe(12)
        with self._lock:
            self._jobs[job_id] = {
                "id": job_id,
                "kind": kind,
                "payload": payload,
                "status": "queued",
                "created_at": time.time(),
                "started_at": None,
                "finished_at": None,
                "output": "",
                "error": None,
            }
        return job_id

    def start(self, job_id):
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job["status"] = "running"
            job["started_at"] = time.time()
            return dict(job)

    def finish(self, job_id, output, error):
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return
            job["status"] = "failed" if error else "done"
            job["finished_at"] = time.time()
            job["output"] = output
            job["error"] = error

    def get(self, job_id):
        with self._lock:
            job = self._jobs.get(job_id)
            return dict(job) if job else None


def _run_scan_job(job_store, job_id):
    job = job_store.start(job_id)
    if not job:
        return

    payload = job["payload"]
    mode = payload.get("mode")
    target = payload.get("target")
    interface = payload.get("interface")
    ports = payload.get("ports")

    output = ""
    error = None
    buf = io.StringIO()
    try:
        from modules.scanner import Scanner

        with redirect_stdout(buf), redirect_stderr(buf):
            Scanner(target=target, interface=interface, mode=mode, ports=ports).start()
        output = buf.getvalue()
    except BaseException as e:
        output = buf.getvalue()
        error = str(e)

    job_store.finish(job_id, output=output, error=error)


def _make_handler(job_store, token):
    class Handler(BaseHTTPRequestHandler):
        def _send_json(self, code, data):
            payload = json.dumps(data).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _send_html(self, code, html):
            payload = html.encode()
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _read_json(self):
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length) if content_length else b""
            if not body:
                return {}
            return json.loads(body.decode())

        def _auth_ok(self):
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                return secrets.compare_digest(auth.removeprefix("Bearer ").strip(), token)
            return False

        def do_GET(self):
            if self.path == "/":
                self._send_html(
                    200,
                    """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>PytheM</title>
  </head>
  <body>
    <h1>PytheM</h1>
    <div>
      <label>Token <input id="token" type="password" style="width: 360px" /></label>
      <button id="saveToken">Save</button>
    </div>
    <hr />
    <h2>Scanner</h2>
    <div>
      <label>Mode
        <select id="mode">
          <option value="tcp">tcp</option>
          <option value="arp">arp</option>
          <option value="manual">manual</option>
        </select>
      </label>
    </div>
    <div><label>Interface <input id="iface" placeholder="eth0" style="width: 360px" /></label></div>
    <div><label>Target <input id="target" placeholder="192.168.1.0/24" style="width: 360px" /></label></div>
    <div><label>Ports (manual) <input id="ports" placeholder="22,80,443" style="width: 360px" /></label></div>
    <button id="run">Run scan</button>
    <pre id="out" style="white-space: pre-wrap; border: 1px solid #ccc; padding: 12px;"></pre>
    <script>
      const tokenEl = document.getElementById("token");
      const outEl = document.getElementById("out");
      tokenEl.value = localStorage.getItem("pythem_token") || "";
      document.getElementById("saveToken").onclick = () => {
        localStorage.setItem("pythem_token", tokenEl.value);
      };
      async function api(path, body) {
        const res = await fetch(path, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + (localStorage.getItem("pythem_token") || "")
          },
          body: JSON.stringify(body || {})
        });
        return await res.json();
      }
      async function pollJob(id) {
        while (true) {
          const res = await fetch("/api/jobs/" + encodeURIComponent(id), {
            headers: { "Authorization": "Bearer " + (localStorage.getItem("pythem_token") || "") }
          });
          const data = await res.json();
          if (data.output) outEl.textContent = data.output;
          if (data.status === "done") return;
          if (data.status === "failed") {
            outEl.textContent = (data.output || "") + "\\n" + (data.error || "failed");
            return;
          }
          await new Promise(r => setTimeout(r, 800));
        }
      }
      document.getElementById("run").onclick = async () => {
        outEl.textContent = "";
        const mode = document.getElementById("mode").value;
        const iface = document.getElementById("iface").value;
        const target = document.getElementById("target").value;
        const ports = document.getElementById("ports").value;
        const payload = { mode, interface: iface, target };
        if (mode === "manual" && ports.trim()) payload.ports = ports;
        const resp = await api("/api/scan", payload);
        if (resp.error) {
          outEl.textContent = resp.error;
          return;
        }
        await pollJob(resp.job_id);
      };
    </script>
  </body>
</html>
""".strip(),
                )
                return

            if self.path == "/api/health":
                self._send_json(200, {"ok": True, "version": version})
                return

            if self.path.startswith("/api/jobs/"):
                if not self._auth_ok():
                    self._send_json(401, {"error": "unauthorized"})
                    return
                job_id = self.path.removeprefix("/api/jobs/").strip("/")
                job = job_store.get(job_id)
                if not job:
                    self._send_json(404, {"error": "not_found"})
                    return
                self._send_json(200, job)
                return

            self._send_json(404, {"error": "not_found"})

        def do_POST(self):
            if self.path == "/api/scan":
                if not self._auth_ok():
                    self._send_json(401, {"error": "unauthorized"})
                    return

                try:
                    body = self._read_json()
                except Exception:
                    self._send_json(400, {"error": "invalid_json"})
                    return

                mode = body.get("mode")
                target = body.get("target")
                interface = body.get("interface")
                ports = body.get("ports")

                if mode not in {"tcp", "arp", "manual"}:
                    self._send_json(400, {"error": "invalid_mode"})
                    return
                if not target or not interface:
                    self._send_json(400, {"error": "target_and_interface_required"})
                    return
                if mode == "manual" and not ports:
                    self._send_json(400, {"error": "ports_required_for_manual"})
                    return

                job_id = job_store.create(
                    kind="scan",
                    payload={
                        "mode": mode,
                        "target": target,
                        "interface": interface,
                        "ports": ports,
                    },
                )
                t = threading.Thread(target=_run_scan_job, args=(job_store, job_id), daemon=True)
                t.start()
                self._send_json(200, {"job_id": job_id})
                return

            self._send_json(404, {"error": "not_found"})

        def log_message(self, format, *args):
            return

    return Handler


def _run_web(host, port, token):
    job_store = _JobStore()
    handler = _make_handler(job_store=job_store, token=token)
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pythem")
    parser.add_argument("--web", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    parser.add_argument("--token", default=None)
    args = parser.parse_args(argv)

    _require_root()

    print(banner(version))
    print(color("by: ", "blue") + color("m4n3dw0lf", "red"))
    print()

    if args.web:
        token = args.token or os.environ.get("PYTHEM_WEB_TOKEN") or secrets.token_urlsafe(24)
        print("[*] Web UI:")
        print("    http://{}:{}/".format(args.host, args.port))
        print("[*] Token:")
        print("    {}".format(token))
        _run_web(host=args.host, port=args.port, token=token)
        return 0

    from core.interface import Processor

    Processor().start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
