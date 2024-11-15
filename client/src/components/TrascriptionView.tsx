export default function TranscriptionView({ transcription }: { transcription: string }) {
    return (
      <div>
        <h1>Transcripción</h1>
        <p>{transcription || "No hay transcripción disponible."}</p>
      </div>
    );
  }
  