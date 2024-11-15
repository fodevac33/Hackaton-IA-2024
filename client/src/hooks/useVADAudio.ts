// @ts-nocheck
import { useMicVAD } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";
import { transcribeAudio } from "../services/transcriptionService";
import { processTextToSpeech } from "../services/ttsService";

ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

const API_URL = import.meta.env.VITE_API_URL;

export function useVADAudio(
  userId: string,
  setMicActive: React.Dispatch<React.SetStateAction<boolean>>,
  idConv: string,
  setIdConv: React.Dispatch<React.SetStateAction<string>>
) {
  const vad = useMicVAD({
    startOnLoad: true,
    onSpeechEnd: async (audio) => {
      try {
        // const result = "Holaa";
        const result = await transcribeAudio(audio);
        console.log("Transcripción recibida:", result);

        if (result) {
          setMicActive(false);

          let body;
          if (idConv) {
            body = JSON.stringify({
              message: result.text,
              user_id: userId,
              chat_id: idConv,
            });
          } else {
            body = JSON.stringify({
              message: result.text,
              user_id: userId,
            });
          }

          const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body,
          });

          console.log(response);

          if (response.ok) {
            const result = await response.json(); // Assuming the response is JSON
            if (result) {
              const url = await processTextToSpeech(result.response);
              setIdConv(result.chat_id);
              const audio = new Audio(url);
              audio.play();

              audio.onended = () => {
                setMicActive(true);
              };
            }
          } else {
            console.error("Failed to fetch data:", response.statusText);
          }
        }
      } catch (error) {
        console.error("Error al procesar el audio:", error);
      }
    },
  });

  return vad;
}
