
copy node_modules\@ricky0123\vad-web\dist\silero_vad.onnx dist
copy node_modules\@ricky0123\vad-web\dist\vad.worklet.bundle.min.js dist
copy node_modules\onnxruntime-web\dist\ort-wasm-simd-threaded.mjs dist

xcopy node_modules\onnxruntime-web\dist\*.wasm dist\ /s /e /y
