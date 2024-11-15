import { useMicVAD } from "@ricky0123/vad-react";
import { ort } from "@ricky0123/vad-web/dist/real-time-vad";

ort.env.wasm.wasmPaths = "https://unpkg.com/onnxruntime-web@dev/dist/";

function App() {
  const vad = useMicVAD({
    startOnLoad: true,
    onSpeechEnd: () => {
      // const wavBuffer = utils.encodeWAV(audio);
      // const base64 = utils.arrayBufferToBase64(wavBuffer);
      // const url = `data:audio/wav;base64,${base64}`;
      // console.log(url);
      console.log("User stopped talking");
    },
  });

  console.log(vad);

  return <div>{vad.userSpeaking ? "User is speaking" : "jjjdsjfdsjdas"}</div>;
}

export default App;
