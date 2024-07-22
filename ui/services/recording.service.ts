export async function submitRecording(recordingBlob: Blob): Promise<{transcription: string}> {
    const formData = new FormData()
    formData.append('recording', recordingBlob)

    const res = await fetch('http://localhost:5000/recordings/transcribe', {method: 'POST', body: formData})

    return res.json()
}

export async function generateNote(transcription: string): Promise<{note: string}> {

    const res = await fetch('http://localhost:5000/recordings/note', 
                            {
                                method: 'POST', 
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({transcription}),
                            } )

    return res.json()
}