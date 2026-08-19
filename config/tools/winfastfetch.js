#!/usr/bin/env node
/**
 * winfastfetch.js - Fake fastfetch output for Windows.
 * Mimics the boxed + nerd-font-icon + palette style of fastfetch.
 * Pure console.log output, all data is randomly fabricated.
 *
 * Usage:
 *   node winfastfetch.js
 */

'use strict';

// ---------------- ANSI helpers ----------------
const R = '\x1b[0m';                       // reset
const B = '\x1b[1m';                       // bold
const C = '\x1b[36m';                      // cyan
const color = !!process.stdout.isTTY;      // disable colors when piped, like real fastfetch
const paint = (code, s) => (color ? code + s + R : s);
const bold = (s) => paint(B + C, s);       // logo + title color
const cyan = (s) => paint(C, s);           // header color
const keyc = (n, s) => paint(B + '\x1b[' + n + 'm', s); // bold + key color
const dot = (n) => paint('\x1b[38;5;' + n + 'm', '\u25CF');

// ---------------- icons (nerd font, as escapes so the source stays pure ASCII) ----------------
const IC = {
  header: '\uE8E5',   // nf-dev-windows11 (Windows 11 logo)
  os: '\uE8E5',      // nf-dev-windows11 (Windows 11 logo)
  kernel: '\uF17C',   // 
  pkg: '\u{F03D7}',   // 
  display: '@',       // literal @
  theme: '\uEB7F',    // 
  cursor: '\u{F01C0}',// 
  font: '\uE659',     // 
  terminal: '\uF489', // 
  user: '\uF007',     // 
  cpu: '\uF4BC',      // 
  gpu: '\u{F02F5}',   // 
  shell: '\uEBCA',    // 
  python: '\uE73C',   // 
  node: '\uE718',     // 
  memory: '\u{F001A}',// 
  osage: '\u{F199F}', // 
  uptime: '\u{F1AD0}',// 
  machine: '\uED0A',  // 
  locale: '\uF031',   // 
};

// ---------------- layout geometry (measured from real fastfetch output) ----------------
const INFO_COL = 41;                        // 0-based column where boxes start
const BOX_TOP = '\u250C' + '\u2500'.repeat(57) + '\u2510';    // box top border
const BOX_BOT = '\u2514' + '\u2500'.repeat(57) + '\u2518';    // box bottom border

// ---------------- windows 11 logo (built-in fastfetch logo, 16 rows) ----------------
const LOGO_ROW = '/////////////////  /////////////////';
const LOGO = Array(16).fill(LOGO_ROW);
const GAP = ' '.repeat(INFO_COL - LOGO_ROW.length);
const PAD = ' '.repeat(INFO_COL);

// ---------------- random helpers ----------------
const rnd = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const pick = (arr) => arr[rnd(0, arr.length - 1)];
const rndStr = (len) => Array.from({ length: len }, () => pick('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')).join('');

// ---------------- hardware presets (coherent combinations) ----------------
const platforms = [
  { host: 'ASUS ROG Strix G16 G614JI', os: 'Windows 11 Pro 24H2 26100.3476', kernel: '10.0.26100.3476',
    cpu: '13th Gen Intel(R) Core(TM) i7-13650HX', gpu: 'NVIDIA GeForce RTX 4060 Laptop GPU', vendor: 'NVIDIA', freq: '2.48', mem: 15.74 },
  { host: 'Micro-Star International Co., Ltd. B650M MORTAR WIFI', os: 'Windows 11 Pro 24H2 26100.3476', kernel: '10.0.26100.3476',
    cpu: 'AMD Ryzen 7 7800X3D', gpu: 'NVIDIA GeForce RTX 4070 SUPER', vendor: 'NVIDIA', freq: '2.53', mem: 31.78 },
  { host: 'LENOVO 21D3 LENOVO', os: 'Windows 11 Home 24H2 26100.3476', kernel: '10.0.26100.3476',
    cpu: 'AMD Ryzen 7 7840HS', gpu: 'AMD Radeon(TM) 780M', vendor: 'AMD', freq: '2.70', mem: 31.19 },
  { host: 'Dell Inc. XPS 15 9530', os: 'Windows 11 Pro 24H2 26100.3476', kernel: '10.0.26100.3476',
    cpu: '13th Gen Intel(R) Core(TM) i7-13700H', gpu: 'NVIDIA GeForce RTX 4070 Laptop GPU', vendor: 'NVIDIA', freq: '2.46', mem: 31.78 },
  { host: 'Gigabyte Technology Co., Ltd. B760M AORUS ELITE', os: 'Windows 10 Pro 22H2 19045.5011', kernel: '10.0.19045.5011',
    cpu: '13th Gen Intel(R) Core(TM) i5-13600KF', gpu: 'NVIDIA GeForce RTX 3060', vendor: 'NVIDIA', freq: '1.83', mem: 31.78 },
  { host: 'Micro-Star International Co., Ltd. PRO B650-P WIFI', os: 'Windows 11 Pro 23H2 22631.4460', kernel: '10.0.22631.4460',
    cpu: 'AMD Ryzen 7 7700X', gpu: 'AMD Radeon(TM) Graphics', vendor: 'AMD', freq: '2.20', mem: 31.78 },
];

// ---------------- random material ----------------
const names = ['flt18355', 'user', 'admin', 'root', 'guest', 'xiaoming'];
const shells = ['pwsh 7.4.6', 'pwsh 7.5.2', 'cmd', 'Windows PowerShell 5.1.22621.4391'];
const terms = ['Windows Terminal', 'WezTerm', 'Windows PowerShell'];
const fonts = ['CaskaydiaCove Nerd Font (14pt)', 'JetBrainsMono Nerd Font (12pt)', 'Cascadia Mono (14pt)', 'Sarasa Mono SC (12pt)'];
const cursors = ['Windows Default (24px)', 'Windows Aero (24px)', 'Windows Black (24px)'];
const locales = ['zh-CN', 'en-US', 'zh-TW', 'ja-JP'];
const displays = [
  { w: 1920, h: 1080, hz: 144 },
  { w: 2560, h: 1600, hz: 165 },
  { w: 3440, h: 1440, hz: 100 },
  { w: 3840, h: 2160, hz: 60 },
];
const pkgMgrSets = [['winget'], ['winget', 'scoop'], ['winget', 'chocolatey']];

// ---------------- assemble a plausible config ----------------
const plat = pick(platforms);
const user = pick(names);
const host = 'DESKTOP-' + rndStr(7);
const display = pick(displays);
const pkgManagers = pick(pkgMgrSets);
const pkgCount = rnd(12, 350);
const memUsed = +(plat.mem * rnd(18, 82) / 100).toFixed(2);
const memPct = Math.round((memUsed / plat.mem) * 100);
const ageDays = rnd(5, 900);
const uptimeMin = rnd(5, 3 * 24 * 60);

function fmtUptime(min) {
  const d = Math.floor(min / 1440);
  const h = Math.floor((min % 1440) / 60);
  const m = min % 60;
  const parts = [];
  if (d) parts.push(d + (d === 1 ? ' day' : ' days'));
  if (h) parts.push(h + (h === 1 ? ' hour' : ' hours'));
  if (m) parts.push(m + (m === 1 ? ' min' : ' mins'));
  return parts.join(', ') || '0 mins';
}

// ---------------- line builders ----------------
const keyLine = (icon, name, col, value) =>
  keyc(col, '  ' + icon + ' ' + name) + ' : ' + value;
const titleLine = () =>
  bold('  ' + IC.user) + ' : ' + bold(user) + '@' + bold(host);
const paletteLine = () =>
  '  ' + [8, 7, 6, 5, 4, 3, 2, 1].map(dot).join(' ');

const infoLines = [
  cyan('  ' + IC.header + '  OS Info'),
  BOX_TOP,
  keyLine(IC.os, 'OS', 31, plat.os),
  keyLine(IC.kernel, 'Kernel', 31, plat.kernel),
  keyLine(IC.pkg, 'Packages', 32, `${pkgCount} (${pkgManagers.join(', ')})`),
  keyLine(IC.display, 'Display', 32, `${display.w}x${display.h} @ ${display.hz}Hz`),
  keyLine(IC.theme, 'Theme', 36, pick(['Dark', 'Light'])),
  keyLine(IC.cursor, 'Cursor', 36, pick(cursors)),
  keyLine(IC.font, 'Font', 33, pick(fonts)),
  keyLine(IC.terminal, 'Terminal', 33, pick(terms)),
  BOX_BOT,
  '', // break
  titleLine(),
  BOX_TOP,
  keyLine(IC.cpu, 'CPU', 34, plat.cpu),
  keyLine(IC.gpu, 'GPU', 34, `${plat.gpu} ${plat.vendor} ${plat.freq} Ghz`),
  keyLine(IC.shell, 'Shell', 35, pick(shells)),
  keyLine(IC.python, 'Python', 35, pick(['Python 3.12.4', 'Python 3.11.9', 'Python 3.13.1'])),
  keyLine(IC.node, 'Node.js', 35, pick(['v22.11.0', 'v20.18.1', 'v23.3.0'])),
  keyLine(IC.memory, 'Memory', 35, `${memUsed.toFixed(2)} GiB / ${plat.mem} GiB (${memPct}%)`),
  keyLine(IC.osage, 'OS Age ', 31, `${ageDays} days`),
  keyLine(IC.uptime, 'Uptime ', 31, fmtUptime(uptimeMin)),
  keyLine(IC.machine, 'Machine', 31, plat.host),
  keyLine(IC.locale, 'locale', 31, pick(locales)),
  BOX_BOT,
  paletteLine(),
  '',
];

// ---------------- print (logo on the left, like fastfetch) ----------------
infoLines.forEach((line, i) => {
  const logoPart = i < LOGO.length ? bold(LOGO[i]) + GAP : PAD;
  console.log(logoPart + line);
});
