'use client'

import { useEffect, useState } from "react";
import { FaMicrophone } from "react-icons/fa";
import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import { submitRecording } from "@/services/recording.service";
import { ClipLoader } from "react-spinners";


export default function Home() {
  const {
    startRecording,
    stopRecording,
    togglePauseResume,
    recordingBlob,
    isRecording,
    isPaused,
    recordingTime,
    mediaRecorder
  } = useAudioRecorder();

  const [transcription, setTranscription] = useState('')
  const [note, setNote] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect( () => {
    if (!recordingBlob) return;
    setLoading(true)
    console.log(recordingBlob)
    submitRecording(recordingBlob)
      .then(res => {
        setTranscription(res.transcription)
        setNote(res.note)
        setLoading(false)
      })

    // recordingBlob will be present at this point after 'stopRecording' has been called
  }, [recordingBlob])
  
  const toggleRecording = (e: any) => {
    if (!isRecording) {
      console.log('Starting Recording')
      startRecording()
    } else {
      console.log('Stopping Recording')
      stopRecording()
    }
  }

  return (
    <>
    <div className="article prose lg:prose-xl flex flex-col items-center">
      <h1>Welcome to the future of AI scribing using open source tools</h1>
      <button onClick={toggleRecording} className={(isRecording ? 'bg-red-900 text-white': '') + ' cursor-pointer text-3xl hover:bg-red-900 hover:text-white rounded-full p-5'}>
        <FaMicrophone />
      </button>
      {isRecording ? <div>{recordingTime}</div> : ''}
      <ClipLoader
        loading={loading}
        size={150}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
      <h3>Transcription</h3>
      {transcription.length ? <p>{transcription}</p> : ''}
      <h3>Note</h3>
      {note.length ? <p>{note}</p> : ''}
    </div>
    </>
  );
}
