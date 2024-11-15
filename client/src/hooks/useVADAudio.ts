import { useMicVAD } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";
import { transcribeAudio } from "../services/transcriptionService";

ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

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
          const response = await fetch(`${api}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ response: Response, userid: userId }),
          });

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
