#!/bin/sh

# Copy the VAD model file
cp node_modules/@ricky0123/vad-web/dist/silero_vad.onnx dist/

# Copy the VAD worklet bundle
cp node_modules/@ricky0123/vad-web/dist/vad.worklet.bundle.min.js dist/

# Copy the ONNX Runtime module
cp node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.mjs dist/

# Copy all `.wasm` files recursively
cp -R node_modules/onnxruntime-web/dist/*.wasm dist/
