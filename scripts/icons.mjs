/** Rasterises public/favicon.svg into the PNG/ICO sizes browsers ask for. */
import sharp from 'sharp';
import { readFileSync, writeFileSync } from 'node:fs';

const svg = readFileSync('public/favicon.svg');
const png = (size) => sharp(svg, { density: 384 }).resize(size, size).png({ compressionLevel: 9 });

await png(180).toFile('public/apple-touch-icon.png');
await png(192).toFile('public/icon-192.png');
await png(512).toFile('public/icon-512.png');

/* A minimal 32x32 single-image .ico for legacy address bars. */
const raw = await sharp(svg, { density: 384 }).resize(32, 32).png({ compressionLevel: 9 }).toBuffer();
const header = Buffer.alloc(22);
header.writeUInt16LE(0, 0);
header.writeUInt16LE(1, 2);
header.writeUInt16LE(1, 4);
header.writeUInt8(32, 6);
header.writeUInt8(32, 7);
header.writeUInt8(0, 8);
header.writeUInt8(0, 9);
header.writeUInt16LE(1, 10);
header.writeUInt16LE(32, 12);
header.writeUInt32LE(raw.length, 14);
header.writeUInt32LE(22, 18);
writeFileSync('public/favicon.ico', Buffer.concat([header, raw]));
console.log('icons written');
