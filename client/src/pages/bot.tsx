import { useState } from "react";
import { useVADAudio } from "../hooks/useVADAudio";
import TranscriptionView from "../components/TrascriptionView";
import { processTextToSpeech } from "../services/ttsService";

export default function App() {
  const [transcription, setTranscription] = useState("");
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const vad = useVADAudio(setTranscription);

  const handleGenerateAudio = async () => {
    if (!transcription) {
      alert("Por favor, transcribe algo primero.");
      return;
    }

    const url = await processTextToSpeech(transcription);
    if (url) {
      setAudioUrl(url);
    } else {
      alert("Error al procesar texto a voz.");
    }
  };

  return (
    <div className="h-screen w-full flex flex-col items-center p-6">
      <h1>Micrófono</h1>
      <button onClick={() => vad.start()}>Iniciar</button>
      <button onClick={() => vad.pause()}>Pausar</button>
      <button onClick={handleGenerateAudio}>Generar Audio</button>
      <TranscriptionView transcription={transcription} />
      {audioUrl && (
        <audio controls autoPlay>
          <source src={audioUrl} type="audio/mpeg" />
          Tu navegador no soporta el elemento de audio.
        </audio>
      )}
    </div>
  );
}
