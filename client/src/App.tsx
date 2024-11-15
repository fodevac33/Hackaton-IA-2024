import { ort } from "@ricky0123/vad-web/dist/real-time-vad";
import { Route, Routes } from "react-router-dom";
import Index from "./pages";
import Bot from "./pages/bot";
import Summary from "./pages/summary";


ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Index />}></Route>
      <Route path="/bot" element={<Bot />}></Route>
      <Route path="/summary" element={<Summary />}></Route>
    </Routes>
  );
}

export default App;
