import { utils } from "@ricky0123/vad-react";

export async function transcribeAudio(audio: Float32Array): Promise<any> {
  // Convierte el audio a formato WAV
  const wavBuffer = utils.encodeWAV(audio);
  const blob = new Blob([wavBuffer], { type: "audio/wav" });

  const formData = new FormData();
  formData.append("file", blob, "audio.wav");
  formData.append("model", "whisper-large-v3-turbo");
  formData.append("temperature", "0");
  formData.append("response_format", "json");
  formData.append("language", "es");

  const GROQ_API_KEY = import.meta.env.VITE_GROQ_API_KEY; 
  if (!GROQ_API_KEY) {
    throw new Error("GROQ_API_KEY no está definida en las variables de entorno");
  }

  const response = await fetch("https://api.groq.com/openai/v1/audio/transcriptions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${GROQ_API_KEY}`,
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Error en la transcripción: ${response.statusText}`);
  }

  return response.json();
}
