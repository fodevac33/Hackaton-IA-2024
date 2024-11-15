import { useMicVAD, utils } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";

// Configuración del entorno ONNX Runtime
ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

function App() {
  const vad = useMicVAD({
    startOnLoad: true,
    onSpeechEnd: async (audio) => {
      try {
        const wavBuffer = utils.encodeWAV(audio);
        const blob = new Blob([wavBuffer], { type: "audio/wav" });

        const formData = new FormData();
        formData.append("file", blob, "audio.wav"); 
        formData.append("model", "whisper-large-v3-turbo"); 
        formData.append("temperature", "0"); 
        formData.append("response_format", "json"); 
        formData.append("language", "es"); 

        // const apiKey = process.env.REACT_APP_GROQ_API_KEY;
        const response = await fetch("https://api.groq.com/openai/v1/audio/transcriptions", {
          method: "POST",
          headers: {
            Authorization: `Bearer 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`, // Clave API desde variables de entorno
          },
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          console.log("Transcripción recibida:", result);
        } else {
          console.error("Error en la transcripción:", response.statusText);
        }
      } catch (error) {
        console.error("Error al procesar el audio:", error);
      }
    },
  });

  return (
    <div>
      {vad.userSpeaking ? "User is speaking" : "No speech detected"}
    </div>
  );
}

export default App;
