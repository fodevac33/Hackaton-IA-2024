// @ts-nocheck
import { useMicVAD } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";
import { transcribeAudio } from "../services/transcriptionService";

ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

const API_URL = import.meta.env.VITE_API_URL;

export function useVADAudio(
  userId: string,
  setMicActive: React.Dispatch<React.SetStateAction<boolean>>
) {
  const vad = useMicVAD({
    startOnLoad: true,
    onSpeechEnd: async (audio) => {
      try {
        const result = await transcribeAudio(audio);
        console.log("Transcripción recibida:", result);

        if (result) {
          const body = JSON.stringify({
            message: result.text,
            user_id: userId,
          });
          console.log(body);
          const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body,
          });

          if (response.ok) {
            const result = await response.json(); // Assuming the response is JSON
            console.log("Response received:", result);
          } else {
            console.error("Failed to fetch data:", response.statusText);
          }
          if (response.body) {
            // const reader = response.body.getReader();
            // // Stream processing
            // while (true) {
            //   const { value, done } = await reader.read();
            //   if (done) break;
            //   if (value) {
            //     setMicActive(true);
            //   }
            // }
          }
        }
      } catch (error) {
        console.error("Error al procesar el audio:", error);
      }
    },
  });

  return vad;
}
