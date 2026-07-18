import zlib
import json
from typing import Dict, Any

class CompressionEngine:
    """
    Phase 6 Optimization: WebSocket Payload Delta Compression
    Intercepts JSON payloads before websocket dispatch and compresses them using zlib
    if they exceed the COMPRESSION_THRESHOLD bytes.
    """
    COMPRESSION_THRESHOLD = 1024  # 1 KB

    @staticmethod
    def compress_payload(payload: Dict[str, Any]) -> bytes:
        json_str = json.dumps(payload)
        raw_bytes = json_str.encode('utf-8')
        
        if len(raw_bytes) > CompressionEngine.COMPRESSION_THRESHOLD:
            compressed = zlib.compress(raw_bytes, level=9)
            # Prefix with magical bytes to signify compression to the frontend
            return b'\x01\x00' + compressed
        
        # Uncompressed raw bytes prefixed with \x00\x00
        return b'\x00\x00' + raw_bytes

    @staticmethod
    def decompress_payload(data: bytes) -> Dict[str, Any]:
        prefix = data[:2]
        payload = data[2:]
        
        if prefix == b'\x01\x00':
            decompressed = zlib.decompress(payload)
            return json.loads(decompressed.decode('utf-8'))
        elif prefix == b'\x00\x00':
            return json.loads(payload.decode('utf-8'))
        else:
            raise ValueError("Unknown payload prefix format.")
