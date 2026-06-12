#!/usr/bin/env node
// control-room serve.mjs — zero-dependency local server.
// Serves dashboard.html and streams ~/.claude/control-room/events.jsonl over SSE.
// Localhost ONLY: events contain work metadata (agent names, task excerpts).
import { createServer } from "node:http";
import { readFileSync, statSync, openSync, readSync, closeSync, existsSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import os from "node:os";

const HOST = "127.0.0.1";
const PORT = Number(process.env.CONTROL_ROOM_PORT || 4517);
const HERE = dirname(fileURLToPath(import.meta.url));
const DASHBOARD = join(HERE, "..", "dashboard.html");
const LOG = join(os.homedir(), ".claude", "control-room", "events.jsonl");
const PIDFILE = join(os.homedir(), ".claude", "control-room", "server.pid");
const REPLAY = 200;
const POLL_MS = 500;
const HEARTBEAT_MS = 15000;

const clients = new Set();
let offset = 0;

function readNew() {
  // Read bytes appended since `offset`; reset on rotation (file shrank).
  let st;
  try { st = statSync(LOG); } catch { return ""; }
  if (st.size < offset) offset = 0;
  if (st.size === offset) return "";
  const fd = openSync(LOG, "r");
  const buf = Buffer.alloc(st.size - offset);
  readSync(fd, buf, 0, buf.length, offset);
  closeSync(fd);
  offset = st.size;
  return buf.toString("utf8");
}

function replayLines() {
  try {
    const all = readFileSync(LOG, "utf8");
    offset = Buffer.byteLength(all);
    return all.split("\n").filter(Boolean).slice(-REPLAY);
  } catch {
    return [];
  }
}

function broadcast(chunk) {
  const lines = chunk.split("\n").filter(Boolean);
  for (const line of lines) {
    const msg = `data: ${line}\n\n`;
    for (const res of clients) res.write(msg);
  }
}

setInterval(() => {
  if (clients.size === 0) return;
  const fresh = readNew();
  if (fresh) broadcast(fresh);
}, POLL_MS);

setInterval(() => {
  for (const res of clients) res.write(`: heartbeat ${Date.now()}\n\n`);
}, HEARTBEAT_MS);

const server = createServer((req, res) => {
  const url = new URL(req.url, `http://${HOST}:${PORT}`);
  if (url.pathname === "/events") {
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    });
    res.write(": connected\n\n");
    for (const line of replayLines()) res.write(`data: ${line}\n\n`);
    res.write(`event: live\ndata: {}\n\n`); // replay done — everything after is real-time
    clients.add(res);
    req.on("close", () => clients.delete(res));
    return;
  }
  if (url.pathname === "/" || url.pathname === "/index.html") {
    try {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(readFileSync(DASHBOARD));
    } catch {
      res.writeHead(500).end("dashboard.html missing");
    }
    return;
  }
  res.writeHead(404).end("not found");
});

server.listen(PORT, HOST, () => {
  try { writeFileSync(PIDFILE, String(process.pid)); } catch {}
  console.log(`control-room live at http://${HOST}:${PORT}/  (events: ${LOG})`);
});
