'use client'

import { useEffect, useState } from "react";
import { FaMicrophone } from "react-icons/fa";
import { AudioRecorder, useAudioRecorder } from 'react-audio-voice-recorder';
import { generateNote, submitRecording } from "@/services/recording.service";
import { ScaleLoader
} from "react-spinners";


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
  const [loadingTranscript, setLoadingTranscript] = useState(false)
  const [loadingNote, setLoadingNote] = useState(false)

  useEffect( () => {
    if (!recordingBlob) return;
    setLoadingTranscript(true)
    console.log(recordingBlob)
    submitRecording(recordingBlob)
      .then(res => {
        setTranscription(res.transcription)
        setLoadingTranscript(false)
        setLoadingNote(true)
        return generateNote(res.transcription)
      })
      .then(res => {
        setNote(res.note)
        setLoadingNote(false)
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
    <div className="article flex flex-col items-center">
      <h1 className="text-white">Welcome to the future of AI scribing using open source tools</h1>
      <button onClick={toggleRecording} className={(isRecording ? 'bg-red-900 text-white': '') + ' cursor-pointer text-3xl hover:bg-red-900 hover:text-white rounded-full p-5'}>
        <FaMicrophone />
      </button>
      {isRecording ? <div>{recordingTime}</div> : ''}
      <div className='flex flex-col items-center p-4 gap-3'>
        <ScaleLoader
          loading={loadingTranscript}
          aria-label="Loading Spinner"
          data-testid="loader"
        />
        {transcription.length ? (
          <>
            <h3>Transcription</h3>
            <p>{transcription}</p>
          </>
          ) : ''}

        <ScaleLoader
          loading={loadingNote}
          aria-label="Loading Spinner"
          data-testid="loader"
        />
        {note.length ? (
          <>
            <h3>Note</h3>
            <p>{note}</p>
          </>
          ) : ''}
      </div>

    </div>
    </>
  );
}
