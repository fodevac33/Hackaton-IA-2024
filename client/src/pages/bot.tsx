import { useVADAudio } from "../hooks/useVADAudio";
import { useState, useEffect } from "react";

function App() {
  const [micActive, setMicActive] = useState(false);

  const vad = useVADAudio();

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

  const handleButtonClick = () => {
    setMicActive((prevState) => !prevState); // Alternar el estado
  };

  return (
    <div>
      <button onClick={handleButtonClick}>
        {micActive ? "Desactivar Micrófono" : "Activar Micrófono"}
      </button>
      <p>{vad.userSpeaking ? "El usuario está hablando..." : "No se detectó habla"}</p>
    </div>
  );
}

export default App;
