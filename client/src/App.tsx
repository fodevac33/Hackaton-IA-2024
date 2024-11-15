import { useState } from "react";
import { useMicVAD } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";
import { transcribeAudio } from "./services/transcriptionService";

// Configuración del entorno ONNX Runtime
ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

function App() {
  const [micActive, setMicActive] = useState(true);

  const vad = useMicVAD({
    startOnLoad: true,
    onSpeechEnd: async (audio) => {
      try {
        const result = await transcribeAudio(audio);
        console.log("Transcripción recibida:", result);
      } catch (error) {
        console.error("Error al procesar el audio:", error);
      }
    },
  });

  const handleButtonClick = () => {
    if (micActive) {
      vad.start(); 
      console.log("Micrófono activado", micActive)
    } else {
      vad.pause(); 
      console.log
    }
    setMicActive(!micActive);
  };

  return (
    <div>
      <button onClick={handleButtonClick}>
        {micActive ? "Desactivar Micrófono" : "Activar Micrófono"}
      </button>
      <p>{vad.userSpeaking ? "El usuario está hablando..." : "No se detectó habla"}</p>
    </div>
  );
}

export default App;
