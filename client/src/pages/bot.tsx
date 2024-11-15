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
    <div>
      <p>
        {vad.userSpeaking
          ? "El usuario está hablando..."
          : "No se detectó habla"}
      </p>
      <p>{response} </p>
      <button onClick={() => handleOnClick()} className="bg-red-600">
        Terminar llamada
      </button>
    </div>
  );
}

export default App;
