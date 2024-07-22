export async function submitRecording(recordingBlob: Blob): Promise<{transcription: string, note: string}> {
    const formData = new FormData()
    formData.append('recording', recordingBlob)

    const res = await fetch('http://localhost:5000/recordings/transcribe', {method: 'POST', body: formData})

    return res.json()
}