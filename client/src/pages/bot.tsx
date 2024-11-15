import { useVADAudio } from "../hooks/useVADAudio";
import { useState, useEffect } from "react";
import initialAudioSrc from "../assets/initialAudio.mp3";
import { useSearchParams } from "react-router-dom";

function App() {
  const [micActive, setMicActive] = useState(false);
  const audio = new Audio(initialAudioSrc);

  const [searchParams] = useSearchParams();
  const clientId = searchParams.get("clientId");

  const vad = useVADAudio(clientId, setMicActive);

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
    audio.play();

    audio.onended = () => {
      setMicActive(true);
    };

    return () => {
      audio.pause();
      audio.currentTime = 0;
    };
  }, []);

  // const handleButtonClick = () => {
  //   const url = "https://api.play.ht/api/v2/tts/stream";
  //   const options = {
  //     method: "POST",
  //     headers: { accept: "audio/mpeg", "content-type": "application/json" },
  //     body: JSON.stringify({
  //       voice:
  //         "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
  //       output_format: "mp3",
  //     }),
  //   };

  //   fetch(url, options)
  //     .then((res) => res.json())
  //     .then((json) => console.log(json))
  //     .catch((err) => console.error(err));
  // };

  return (
    <div>
      <button onClick={handleButtonClick}>send</button>
      <p>
        {vad.userSpeaking
          ? "El usuario está hablando..."
          : "No se detectó habla"}
      </p>
    </div>
  );
}

export default App;
