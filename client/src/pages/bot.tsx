import { useMicVAD } from "@ricky0123/vad-react";

export default function Bot() {
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
  return <div>bot</div>;
}
