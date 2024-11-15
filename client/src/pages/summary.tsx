import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function Summary() {
  const API_URL = import.meta.env.VITE_API_URL;

  const [sentiment, setSentiment] = useState("");
  const [score, setScore] = useState("");

  const [searchParams] = useSearchParams();
  const chatId = searchParams.get("chatId");

  useEffect(() => {
    const fetchChatData = async () => {
      try {
        const response = await fetch(`${API_URL}/sentiment`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: chatId,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setSentiment(data.justification);
          setScore(data.rating);
        } else {
          console.error("Failed to fetch chat data:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching chat data:", error);
      }
    };

    if (chatId) {
      fetchChatData();
    }
  }, [API_URL, chatId]);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white shadow-md rounded-lg p-8 text-center">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">
          Sentiment Analysis
        </h1>
        <p className="text-lg text-gray-600 mb-2">
          <span className="font-semibold">Justification:</span> {sentiment}
        </p>
        <p className="text-lg text-gray-600">
          <span className="font-semibold">Score:</span> {score}
        </p>
      </div>
    </div>
  );
}
