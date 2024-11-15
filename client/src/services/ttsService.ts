import axios from "axios";

const elevenLabsAPIKey = import.meta.env.VITE_ELEVENLABS_API_KEY;
const elevenLabsURL =
  "https://api.elevenlabs.io/v1/text-to-speech/FGY2WhTYpPnrIDTdsKH5";

export const processTextToSpeech = async (
  text: string
): Promise<string | null> => {
  try {
    const response = await axios.post(
      elevenLabsURL,
      {
        text,
        model_id: "eleven_multilingual_v1",
        voice_settings: {
          stability: 0.55,
          similarity_boost: 0.55,
        },
      },
      {
        headers: {
          Accept: "audio/mpeg",
          "Content-Type": "application/json",
          "xi-api-key": elevenLabsAPIKey,
        },
        responseType: "arraybuffer", // Important to handle audio data
      }
    );

    // Convert the binary audio data to a blob URL
    const blob = new Blob([response.data], { type: "audio/mpeg" });
    return URL.createObjectURL(blob); // Return the blob URL
  } catch (error) {
    console.error("Error during text-to-speech processing:", error);
    return null;
  }
};
