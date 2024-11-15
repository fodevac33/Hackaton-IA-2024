import { useMicVAD } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";
import { transcribeAudio } from "../services/transcriptionService";

ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

export function useVADAudio(onTranscriptionUpdate: (transcription: string) => void) {
  const vad = useMicVAD({
    startOnLoad: true,
    onSpeechEnd: async (audio) => {
      try {
        const result = await transcribeAudio(audio);
        console.log("Transcripción recibida:", result);
        onTranscriptionUpdate(result.text);
      } catch (error) {
        console.error("Error al procesar el audio:", error);
      }
    },
  });

  return vad;
}


