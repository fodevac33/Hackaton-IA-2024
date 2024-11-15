// @ts-nocheck
import { useVADAudio } from "../hooks/useVADAudio";
import { useState, useEffect } from "react";
import initialAudioSrc from "../assets/initialAudio.mp3";
import { useSearchParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function App() {
  const [micActive, setMicActive] = useState(false);
  const navigate = useNavigate();

  const [idConv, setIdConv] = useState("");
  const [response, setReponse] = useState("");

  const [searchParams] = useSearchParams();
  const clientId = searchParams.get("clientId");

  const vad = useVADAudio(
    clientId,
    setMicActive,
    idConv,
    setIdConv,
    setReponse
  );

  // Efecto para controlar el estado del micrófono basado en micActive
  useEffect(() => {
    if (micActive) {
      vad.start(); // Iniciar el micrófono
      console.log("Micrófono activado");
    } else {
      vad.pause(); // Pausar el micrófono
      console.log("Micrófono desactivado");
    }
  }, [micActive, vad]);

  useEffect(() => {
    const audio = new Audio(initialAudioSrc);

    audio.play();

    audio.onended = () => {
      setMicActive(true);
    };

    return () => {
      audio.pause();
      audio.currentTime = 0;
    };
  }, []);

  const handleOnClick = () => {
    navigate(`/summary?chatId=${idConv}`);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-gray-800">
      <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-md text-center">
        <h1 className="text-2xl font-bold mb-4">Asistente de Voz</h1>
        <p className="text-lg mb-4">
          {vad.userSpeaking
            ? "🎙️ El usuario está hablando..."
            : "🤔 No se detectó habla"}
        </p>
        <p className="text-gray-600 mb-6">
          {response || "Esperando respuesta..."}
        </p>
        <button
          onClick={handleOnClick}
          className="bg-red-600 text-white py-2 px-4 rounded-lg shadow-md hover:bg-red-700 transition duration-300"
        >
          Terminar llamada
        </button>
      </div>
    </div>
  );
}

export default App;
