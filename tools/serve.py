#!/usr/bin/env python3
"""Tiny static file server for the Proxima web app.

Reads the port from the PORT environment variable (which the preview harness
injects, and can relocate via autoPort) and falls back to 7799 for manual runs.
Serves proxima/web/ regardless of the current working directory.
"""
import functools
import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", "7799"))
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")

socketserver.TCPServer.allow_reuse_address = True  # avoid TIME_WAIT collisions
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Proxima serving {os.path.normpath(DIRECTORY)} on :{PORT}")
    httpd.serve_forever()
