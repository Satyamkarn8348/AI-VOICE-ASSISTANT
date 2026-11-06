import { useEffect, useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './App.css'

// Backend API
const API_URL = 'http://127.0.0.1:8002'

// ==========================================
// 3D ROBOT COMPONENT
// ==========================================

function Robot({ mode }) {
  const rootRef = useRef()
  const headRef = useRef()
  const leftArmRef = useRef()
  const rightArmRef = useRef()
  const mouthRef = useRef()
  const leftEyeRef = useRef()
  const rightEyeRef = useRef()

  useFrame((state) => {
    const t = state.clock.elapsedTime

    if (rootRef.current) {
      rootRef.current.position.y = Math.sin(t * 1.25) * 0.07
      rootRef.current.rotation.y = Math.sin(t * 0.35) * 0.08
    }

    if (headRef.current) {
      headRef.current.rotation.y = Math.sin(t * 0.65) * 0.1
      headRef.current.rotation.z =
        mode === 'happy' ? Math.sin(t * 3) * 0.08 : 0
    }

    if (leftArmRef.current) {
      leftArmRef.current.rotation.z =
        mode === 'happy'
          ? -0.75 + Math.sin(t * 5) * 0.12
          : -0.18 + Math.sin(t * 1.2) * 0.035
    }

    if (rightArmRef.current) {
      rightArmRef.current.rotation.z =
        mode === 'happy'
          ? 0.75 - Math.sin(t * 5) * 0.12
          : 0.18 + Math.sin(t * 1.2) * 0.035
    }

    const blink =
      t % 4.5 > 4.28 && t % 4.5 < 4.42 ? 0.12 : 1

    if (leftEyeRef.current) {
      leftEyeRef.current.scale.y = blink
    }

    if (rightEyeRef.current) {
      rightEyeRef.current.scale.y = blink
    }

    if (mouthRef.current) {
      mouthRef.current.scale.y =
        mode === 'speaking'
          ? 0.18 + Math.abs(Math.sin(t * 11)) * 0.22
          : mode === 'happy'
            ? 0.16
            : 0.07
    }
  })

  const glow =
    mode === 'thinking'
      ? '#ffb347'
      : mode === 'listening'
        ? '#00eaff'
        : mode === 'happy'
          ? '#62ffad'
          : '#39cfff'

  const shell = '#dce8f2'
  const dark = '#102438'

  return (
    <group ref={rootRef} scale={1.12}>

      {/* BODY */}

      <mesh position={[0, -0.92, 0]}>
        <capsuleGeometry args={[0.48, 0.62, 8, 18]} />
        <meshStandardMaterial
          color={shell}
          metalness={0.82}
          roughness={0.22}
        />
      </mesh>

      {/* CHEST PANEL */}

      <mesh position={[0, -0.83, 0.43]}>
        <boxGeometry args={[0.48, 0.32, 0.08]} />
        <meshStandardMaterial
          color={dark}
          metalness={0.5}
          roughness={0.25}
        />
      </mesh>

      <mesh position={[0, -0.83, 0.49]}>
        <sphereGeometry args={[0.075, 20, 20]} />
        <meshStandardMaterial
          color={glow}
          emissive={glow}
          emissiveIntensity={2.5}
        />
      </mesh>

      {/* SHOULDERS */}

      <mesh position={[-0.58, -0.48, 0]}>
        <sphereGeometry args={[0.22, 24, 24]} />
        <meshStandardMaterial
          color="#9fb5c8"
          metalness={0.8}
          roughness={0.25}
        />
      </mesh>

      <mesh position={[0.58, -0.48, 0]}>
        <sphereGeometry args={[0.22, 24, 24]} />
        <meshStandardMaterial
          color="#9fb5c8"
          metalness={0.8}
          roughness={0.25}
        />
      </mesh>

      {/* LEFT ARM */}

      <group ref={leftArmRef} position={[-0.62, -0.48, 0]}>
        <mesh position={[-0.04, -0.34, 0]}>
          <capsuleGeometry args={[0.13, 0.52, 8, 16]} />
          <meshStandardMaterial
            color={shell}
            metalness={0.8}
            roughness={0.24}
          />
        </mesh>

        <mesh position={[-0.04, -0.68, 0]}>
          <sphereGeometry args={[0.16, 24, 24]} />
          <meshStandardMaterial
            color="#8fa8bd"
            metalness={0.8}
          />
        </mesh>
      </group>

      {/* RIGHT ARM */}

      <group ref={rightArmRef} position={[0.62, -0.48, 0]}>
        <mesh position={[0.04, -0.34, 0]}>
          <capsuleGeometry args={[0.13, 0.52, 8, 16]} />
          <meshStandardMaterial
            color={shell}
            metalness={0.8}
            roughness={0.24}
          />
        </mesh>

        <mesh position={[0.04, -0.68, 0]}>
          <sphereGeometry args={[0.16, 24, 24]} />
          <meshStandardMaterial
            color="#8fa8bd"
            metalness={0.8}
          />
        </mesh>
      </group>

      {/* NECK */}

      <mesh position={[0, -0.05, 0]}>
        <cylinderGeometry args={[0.17, 0.2, 0.3, 24]} />
        <meshStandardMaterial
          color="#8299ad"
          metalness={0.85}
        />
      </mesh>

      {/* HEAD */}

      <group ref={headRef} position={[0, 0.48, 0]}>

        <mesh>
          <sphereGeometry args={[0.78, 40, 40]} />
          <meshStandardMaterial
            color={shell}
            metalness={0.82}
            roughness={0.2}
          />
        </mesh>

        {/* FACE VISOR */}

        <mesh
          position={[0, -0.02, 0.61]}
          scale={[1, 0.7, 0.28]}
        >
          <sphereGeometry args={[0.68, 40, 32]} />
          <meshStandardMaterial
            color={dark}
            metalness={0.45}
            roughness={0.2}
          />
        </mesh>

        {/* LEFT EYE */}

        <group ref={leftEyeRef} position={[-0.25, 0.12, 0.79]}>
          <mesh scale={[1.2, 1, 0.5]}>
            <sphereGeometry args={[0.105, 24, 24]} />
            <meshStandardMaterial
              color={glow}
              emissive={glow}
              emissiveIntensity={3.5}
            />
          </mesh>
        </group>

        {/* RIGHT EYE */}

        <group ref={rightEyeRef} position={[0.25, 0.12, 0.79]}>
          <mesh scale={[1.2, 1, 0.5]}>
            <sphereGeometry args={[0.105, 24, 24]} />
            <meshStandardMaterial
              color={glow}
              emissive={glow}
              emissiveIntensity={3.5}
            />
          </mesh>
        </group>

        {/* MOUTH */}

        <mesh
          ref={mouthRef}
          position={[0, -0.22, 0.79]}
          scale={[1.5, 0.1, 0.45]}
        >
          <sphereGeometry args={[0.09, 24, 24]} />
          <meshStandardMaterial
            color={glow}
            emissive={glow}
            emissiveIntensity={2}
          />
        </mesh>

        {/* ANTENNA */}

        <mesh position={[0, 0.83, 0]}>
          <cylinderGeometry args={[0.025, 0.04, 0.24, 16]} />
          <meshStandardMaterial
            color="#9fb5c8"
            metalness={0.8}
          />
        </mesh>

        <mesh position={[0, 0.99, 0]}>
          <sphereGeometry args={[0.075, 20, 20]} />
          <meshStandardMaterial
            color={glow}
            emissive={glow}
            emissiveIntensity={3}
          />
        </mesh>

        {/* EARS */}

        <mesh position={[-0.78, 0, 0]}>
          <cylinderGeometry args={[0.17, 0.17, 0.16, 24]} />
          <meshStandardMaterial
            color="#91a9bd"
            metalness={0.85}
          />
        </mesh>

        <mesh position={[0.78, 0, 0]}>
          <cylinderGeometry args={[0.17, 0.17, 0.16, 24]} />
          <meshStandardMaterial
            color="#91a9bd"
            metalness={0.85}
          />
        </mesh>

      </group>
    </group>
  )
}

// ==========================================
// MAIN APP
// ==========================================

function App() {
  const [mode, setMode] = useState('idle')
  const [conversationId, setConversationId] = useState(null)

  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isConversationActive, setIsConversationActive] = useState(false)

  const [error, setError] = useState('')
  const [userMessage, setUserMessage] = useState('')
  const [aiMessage, setAiMessage] = useState('')
  const [pendingAudioUrl, setPendingAudioUrl] = useState('')

  const [textInput, setTextInput] = useState('')
  const [relatedQuestions, setRelatedQuestions] = useState([])

  const initializedRef = useRef(false)
  const conversationActiveRef = useRef(false)
  const processingRef = useRef(false)

  const recorderRef = useRef(null)
  const streamRef = useRef(null)
  const audioChunksRef = useRef([])

  const audioRef = useRef(null)
  const audioUrlRef = useRef(null)

  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const sourceRef = useRef(null)
  const animationFrameRef = useRef(null)

  const speechDetectedRef = useRef(false)
  const speechFramesRef = useRef(0)
  const lastSoundTimeRef = useRef(0)
  const recordingStartTimeRef = useRef(0)

  // ==========================================
  // AUDIO CLEANUP
  // ==========================================

  function clearAudioResources() {
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current = null
    }

    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current)
      audioUrlRef.current = null
    }
  }

  // ==========================================
  // MICROPHONE CLEANUP
  // ==========================================

  function cleanupMicrophone() {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current)
      animationFrameRef.current = null
    }

    if (recorderRef.current?.state === 'recording') {
      recorderRef.current.stop()
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }

    if (audioContextRef.current) {
      audioContextRef.current.close().catch(console.error)
      audioContextRef.current = null
    }

    analyserRef.current = null
    sourceRef.current = null
  }

  // ==========================================
  // PLAY AUDIO
  // ==========================================

  async function playAudioBlob(audioBlob) {
    clearAudioResources()

    const audioUrl = URL.createObjectURL(audioBlob)
    audioUrlRef.current = audioUrl

    const audio = new Audio(audioUrl)
    audioRef.current = audio

    setMode('speaking')

    try {
      await new Promise((resolve, reject) => {
        audio.onended = resolve

        audio.onerror = () => reject(
          new Error('Audio play nahi ho payi.')
        )

        audio.play().catch(reject)
      })

      if (audioUrlRef.current === audioUrl) {
        URL.revokeObjectURL(audioUrl)
        audioUrlRef.current = null
      }

      audioRef.current = null
      setPendingAudioUrl('')

      return true

    } catch (playError) {
      audio.pause()
      audioRef.current = null

      setPendingAudioUrl(audioUrl)

      setError(
        'Automatic audio playback block hua. Play Robot Answer button dabao.'
      )

      console.error(playError)

      return false
    }
  }

  // ==========================================
  // SPEAK TEXT
  // ==========================================

  async function speakText(text) {
    const response = await fetch(`${API_URL}/voice/speak`, {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify({ text }),
    })

    if (!response.ok) {
      throw new Error('AI voice generate nahi hui.')
    }

    const audioBlob = await response.blob()

    return playAudioBlob(audioBlob)
  }

  // ==========================================
  // PLAY PENDING AUDIO
  // ==========================================

  async function playPendingAudio() {
    if (!pendingAudioUrl) return

    setError('')

    if (streamRef.current) {
      streamRef.current.getAudioTracks().forEach((track) => {
        track.enabled = false
      })
    }

    const audio = new Audio(pendingAudioUrl)
    audioRef.current = audio

    setMode('speaking')

    try {
      await new Promise((resolve, reject) => {
        audio.onended = resolve

        audio.onerror = () => reject(
          new Error('Audio play nahi ho payi.')
        )

        audio.play().catch(reject)
      })

      setMode('happy')

      setTimeout(() => {
        if (conversationActiveRef.current) {
          setMode('listening')
        } else {
          setMode('idle')
        }
      }, 800)

    } catch (playError) {
      console.error(playError)

      setError('Audio play nahi ho payi. Dobara try karo.')

      setMode('idle')

    } finally {
      audioRef.current = null

      if (audioUrlRef.current === pendingAudioUrl) {
        URL.revokeObjectURL(pendingAudioUrl)
        audioUrlRef.current = null
      }

      setPendingAudioUrl('')

      if (conversationActiveRef.current && streamRef.current) {
        streamRef.current.getAudioTracks().forEach((track) => {
          track.enabled = true
        })
      }
    }
  }

  // ==========================================
  // INITIALIZE ASSISTANT
  // ==========================================

  useEffect(() => {
    if (initializedRef.current) return

    initializedRef.current = true

    async function initializeAssistant() {
      setMode('thinking')
      setError('')

      try {
        const response = await fetch(`${API_URL}/conversations/`, {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify({
            user_id: 2,
            title: 'Satyam AI Assistant',
          }),
        })

        if (!response.ok) {
          throw new Error('Conversation create nahi ho paya.')
        }

        const data = await response.json()

        setConversationId(data.id)

        const greeting = 'Hi Satyam! Tum kaise ho?'

        setAiMessage(greeting)

        const played = await speakText(greeting)

        if (played) {
          setMode('happy')

          setTimeout(() => {
            setMode('idle')
          }, 1000)

        } else {
          setMode('idle')
        }

      } catch (err) {
        setError(err.message || 'Backend connection error.')

        console.error(err)

        setMode('idle')
      }
    }

    initializeAssistant()

    return () => {
      conversationActiveRef.current = false

      cleanupMicrophone()
      clearAudioResources()
    }
  }, [])

  // ==========================================
  // SEND TEXT MESSAGE
  // ==========================================

  async function sendTextMessage(message) {
    const cleanMessage = message.trim()

    if (
      !cleanMessage ||
      !conversationId ||
      processingRef.current
    ) {
      return
    }

    processingRef.current = true

    setIsProcessing(true)
    setTextInput('')
    setUserMessage(cleanMessage)
    setAiMessage('')
    setRelatedQuestions([])
    setError('')
    setMode('thinking')

    clearAudioResources()
    setPendingAudioUrl('')

    if (streamRef.current) {
      streamRef.current.getAudioTracks().forEach((track) => {
        track.enabled = false
      })
    }

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json',
        },

        body: JSON.stringify({
          conversation_id: conversationId,
          message: cleanMessage,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))

        throw new Error(
          errorData.detail || 'AI response nahi mila.'
        )
      }

      const data = await response.json()

      const answer = data.response?.trim()

      if (!answer) {
        throw new Error('AI ne empty response diya.')
      }

      setAiMessage(answer)

      setRelatedQuestions(
        Array.isArray(data.related_questions)
          ? data.related_questions.slice(0, 3)
          : []
      )

      const played = await speakText(answer)

      if (played) {
        setMode('happy')

        setTimeout(() => {
          setMode(
            conversationActiveRef.current
              ? 'listening'
              : 'idle'
          )
        }, 800)

      } else {
        setMode('idle')
      }

    } catch (err) {
      setError(err.message || 'Message send nahi hua.')

      console.error(err)

      setMode('idle')

    } finally {
      processingRef.current = false

      setIsProcessing(false)

      if (
        conversationActiveRef.current &&
        streamRef.current &&
        !audioUrlRef.current
      ) {
        streamRef.current.getAudioTracks().forEach((track) => {
          track.enabled = true
        })

        speechDetectedRef.current = false
        speechFramesRef.current = 0
        lastSoundTimeRef.current = 0

        setMode('listening')
      }
    }
  }

  // ==========================================
  // TEXT FORM
  // ==========================================

  function handleTextSend(event) {
    event.preventDefault()

    sendTextMessage(textInput)
  }

  function handleSuggestedQuestion(question) {
    sendTextMessage(question)
  }

  // ==========================================
  // PROCESS VOICE RECORDING
  // ==========================================

  async function processVoiceRecording(blob) {
    if (!conversationId) {
      throw new Error('Conversation abhi ready nahi hai.')
    }

    if (!blob || blob.size < 2500) {
      console.warn('Audio too small:', blob?.size)

      setError(
        'Audio bahut chhoti hai. Thoda clearly aur lamba boliye.'
      )

      return
    }

    if (processingRef.current) return

    processingRef.current = true

    setIsProcessing(true)
    setMode('thinking')
    setError('')

    if (streamRef.current) {
      streamRef.current.getAudioTracks().forEach((track) => {
        track.enabled = false
      })
    }

    try {
      console.log('Recorded Audio Details:', {
        size: blob.size,
        type: blob.type,
      })

      const formData = new FormData()

      formData.append(
        'conversation_id',
        String(conversationId)
      )

      formData.append('file', blob, 'recording.webm')

      const response = await fetch(`${API_URL}/voice/ask`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))

        throw new Error(
          errorData.detail ||
          'Voice assistant response nahi de paya.'
        )
      }

      const data = await response.json()

      const recognizedText = data.transcribed_text?.trim()
      const answer = data.response?.trim()

      if (!recognizedText) {
        throw new Error('Aapki voice samajh nahi aayi.')
      }

      setUserMessage(recognizedText)
      setAiMessage(answer || '')

      setRelatedQuestions(
        Array.isArray(data.related_questions)
          ? data.related_questions.slice(0, 3)
          : []
      )

      if (!data.audio_base64) {
        throw new Error(
          'AI answer aa gaya, lekin audio nahi mili.'
        )
      }

      const binaryString = window.atob(data.audio_base64)

      const bytes = new Uint8Array(binaryString.length)

      for (
        let index = 0;
        index < binaryString.length;
        index += 1
      ) {
        bytes[index] = binaryString.charCodeAt(index)
      }

      const audioBlob = new Blob([bytes], {
        type: 'audio/mpeg',
      })

      await playAudioBlob(audioBlob)

    } catch (err) {
      setError(err.message || 'Something went wrong.')

      console.error(err)

    } finally {
      processingRef.current = false

      setIsProcessing(false)

      if (
        conversationActiveRef.current &&
        streamRef.current
      ) {
        if (!audioUrlRef.current) {
          streamRef.current.getAudioTracks().forEach((track) => {
            track.enabled = true
          })

          speechDetectedRef.current = false
          speechFramesRef.current = 0
          lastSoundTimeRef.current = 0

          setMode('listening')
        }

      } else {
        cleanupMicrophone()
        setMode('idle')
      }
    }
  }

  // ==========================================
  // START UTTERANCE RECORDING
  // ==========================================

  function startUtteranceRecording() {
    if (
      !conversationActiveRef.current ||
      processingRef.current ||
      recorderRef.current
    ) {
      return
    }

    try {
      const stream = streamRef.current

      if (!stream) return

      let mimeType = ''

      if (
        MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
      ) {
        mimeType = 'audio/webm;codecs=opus'

      } else if (
        MediaRecorder.isTypeSupported('audio/webm')
      ) {
        mimeType = 'audio/webm'
      }

      const recorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream)

      audioChunksRef.current = []

      recorderRef.current = recorder

      recordingStartTimeRef.current = performance.now()

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      recorder.onstop = async () => {
        const recordingBlob = new Blob(
          audioChunksRef.current,
          {
            type: recorder.mimeType || 'audio/webm',
          }
        )

        const recordingDuration =
          performance.now() - recordingStartTimeRef.current

        console.log('Recording finished:', {
          size: recordingBlob.size,
          duration: recordingDuration,
          type: recordingBlob.type,
        })

        recorderRef.current = null

        speechDetectedRef.current = false
        speechFramesRef.current = 0
        lastSoundTimeRef.current = 0

        setIsRecording(false)

        if (
          recordingBlob.size >= 2500 &&
          recordingDuration >= 700
        ) {
          await processVoiceRecording(recordingBlob)

        } else if (conversationActiveRef.current) {
          setMode('listening')

        } else {
          cleanupMicrophone()
          setMode('idle')
        }
      }

      recorder.onerror = (event) => {
        console.error('Recorder error:', event)

        setError('Recording mein problem aayi.')

        recorderRef.current = null
        setIsRecording(false)

        speechDetectedRef.current = false
      }

      recorder.start(250)

      setIsRecording(true)
      setMode('listening')

      lastSoundTimeRef.current = performance.now()

    } catch (err) {
      console.error(err)

      setError('Recording start nahi ho payi.')
    }
  }

  // ==========================================
  // SPEECH DETECTION
  // ==========================================

  function detectSpeech() {
    if (!conversationActiveRef.current) return

    const analyser = analyserRef.current

    if (!analyser) return

    if (processingRef.current) {
      animationFrameRef.current =
        requestAnimationFrame(detectSpeech)

      return
    }

    const audioData = new Uint8Array(analyser.fftSize)

    analyser.getByteTimeDomainData(audioData)

    let sum = 0

    for (
      let index = 0;
      index < audioData.length;
      index += 1
    ) {
      const sample = (audioData[index] - 128) / 128

      sum += sample * sample
    }

    const rms = Math.sqrt(sum / audioData.length)

    const now = performance.now()

    const voiceThreshold = 0.018

    if (recorderRef.current?.state === 'recording') {
      if (rms > voiceThreshold) {
        lastSoundTimeRef.current = now
      }

      if (
        speechDetectedRef.current &&
        now - lastSoundTimeRef.current > 1500
      ) {
        recorderRef.current.stop()
      }

    } else {
      if (rms > voiceThreshold) {
        speechFramesRef.current += 1

        if (speechFramesRef.current >= 4) {
          speechDetectedRef.current = true

          lastSoundTimeRef.current = now

          startUtteranceRecording()
        }

      } else {
        speechFramesRef.current = 0
      }
    }

    animationFrameRef.current =
      requestAnimationFrame(detectSpeech)
  }

  // ==========================================
  // START CONVERSATION
  // ==========================================

  async function startConversation() {
    try {
      setError('')
      setPendingAudioUrl('')

      if (!conversationId) {
        throw new Error('Conversation abhi ready nahi hai.')
      }

      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error(
          'Browser microphone support nahi karta.'
        )
      }

      if (typeof MediaRecorder === 'undefined') {
        throw new Error(
          'Browser recording support nahi karta.'
        )
      }

      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
          },
        })

      streamRef.current = stream

      const AudioContextClass =
        window.AudioContext || window.webkitAudioContext

      if (!AudioContextClass) {
        throw new Error(
          'Browser audio detection support nahi karta.'
        )
      }

      const audioContext = new AudioContextClass()

      audioContextRef.current = audioContext

      if (audioContext.state === 'suspended') {
        await audioContext.resume()
      }

      const analyser = audioContext.createAnalyser()

      analyser.fftSize = 2048
      analyser.smoothingTimeConstant = 0.3

      const source =
        audioContext.createMediaStreamSource(stream)

      source.connect(analyser)

      analyserRef.current = analyser
      sourceRef.current = source

      conversationActiveRef.current = true
      processingRef.current = false

      setIsConversationActive(true)
      setIsRecording(false)
      setIsProcessing(false)
      setMode('listening')

      speechDetectedRef.current = false
      speechFramesRef.current = 0
      lastSoundTimeRef.current = 0

      detectSpeech()

    } catch (err) {
      console.error(err)

      setError(err.message || 'Microphone start nahi hua.')

      conversationActiveRef.current = false

      setIsConversationActive(false)

      cleanupMicrophone()

      setMode('idle')
    }
  }

  // ==========================================
  // STOP CONVERSATION
  // ==========================================

  function stopConversation() {
    conversationActiveRef.current = false

    setIsConversationActive(false)

    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current)

      animationFrameRef.current = null
    }

    if (recorderRef.current?.state === 'recording') {
      recorderRef.current.stop()

    } else if (!processingRef.current) {
      cleanupMicrophone()

      setIsRecording(false)

      setMode('idle')
    }

    setError('')
  }

  // ==========================================
  // CONVERSATION BUTTON
  // ==========================================

  function handleConversationButton() {
    if (conversationActiveRef.current) {
      stopConversation()

    } else {
      startConversation()
    }
  }

  // ==========================================
  // ROBOT MODES
  // ==========================================

  const modes = [
    'idle',
    'listening',
    'thinking',
    'speaking',
    'happy',
  ]

  // ==========================================
  // MAIN UI
  // ==========================================

  return (
    <div className="app">

      <div className="ambient-orb ambient-orb-one" />
      <div className="ambient-orb ambient-orb-two" />
      <div className="background-grid" />

      {/* HEADER */}

      <header className="header">
        <h1>AI Robot Assistant</h1>
        <p>Your personal AI companion</p>
      </header>

      {/* MAIN TWO COLUMN LAYOUT */}

      <main className="main-content">

        {/* LEFT SIDE ROBOT */}

        <section className="robot-section">

          <div className="robot-status">
            <span className={`status-dot ${mode}`} />
            {mode.toUpperCase()}
          </div>

          <div className="robot-canvas">

            <Canvas
              camera={{
                position: [0, 0, 5.5],
                fov: 45,
              }}
            >
              <ambientLight intensity={1.5} />

              <directionalLight
                position={[3, 4, 5]}
                intensity={2}
              />

              <pointLight
                position={[-3, 2, 3]}
                intensity={2}
                color="#FF9933"
              />

              <Robot mode={mode} />

              <OrbitControls
                enableZoom={false}
                enablePan={false}
                minPolarAngle={Math.PI / 2.5}
                maxPolarAngle={Math.PI / 1.8}
              />
            </Canvas>

          </div>

          <p className="robot-message">
            {mode === 'idle' &&
              'Hello! I am ready to help you.'}

            {mode === 'listening' &&
              'I am listening to you...'}

            {mode === 'thinking' &&
              'Let me think about it...'}

            {mode === 'speaking' &&
              'I am speaking to you...'}

            {mode === 'happy' &&
              'I am happy to help you!'}
          </p>

          {/* VOICE CONTROLS */}

          <div className="voice-controls">

            <button
              onClick={handleConversationButton}
              disabled={!conversationId || isProcessing}
            >
              {isConversationActive
                ? '⏹ Stop Conversation'
                : '🎤 Start Conversation'}
            </button>

            {pendingAudioUrl && (
              <button onClick={playPendingAudio}>
                🔊 Play Robot Answer
              </button>
            )}

          </div>

          {/* ROBOT MODES */}

          <div className="mode-buttons">

            {modes.map((item) => (
              <button
                key={item}
                className={mode === item ? 'active' : ''}
                onClick={() => setMode(item)}
                disabled={
                  isConversationActive || isProcessing
                }
              >
                {item}
              </button>
            ))}

          </div>

        </section>

        {/* RIGHT SIDE CHAT */}

        <section className="text-chat-section">

          <h3>Chat with Robot</h3>

          {/* CHAT INPUT */}

          <form
            className="text-chat-form"
            onSubmit={handleTextSend}
          >

            <input
              type="text"
              value={textInput}
              onChange={(event) =>
                setTextInput(event.target.value)
              }
              placeholder="Robot se kuch bhi poochho..."
              disabled={!conversationId || isProcessing}
            />

            <button
              type="submit"
              disabled={
                !textInput.trim() ||
                !conversationId ||
                isProcessing
              }
            >
              {isProcessing ? 'Please wait...' : 'Send'}
            </button>

          </form>

          {/* USER MESSAGE */}

          {userMessage && (
            <div className="conversation-message">

              <strong>You:</strong>

              <p>{userMessage}</p>

            </div>
          )}

          {/* ROBOT ANSWER */}

          {aiMessage && (
            <div className="conversation-message">

              <strong>Robot:</strong>

              <div className="markdown-content">

                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {aiMessage}
                </ReactMarkdown>

              </div>

            </div>
          )}

          {/* RELATED QUESTIONS */}

          {relatedQuestions.length > 0 && (
            <div className="related-questions">

              <p>Related questions</p>

              <div className="related-question-list">

                {relatedQuestions.map((question, index) => (
                  <button
                    type="button"
                    key={`${question}-${index}`}
                    onClick={() =>
                      handleSuggestedQuestion(question)
                    }
                    disabled={isProcessing}
                  >
                    {question}
                  </button>
                ))}

              </div>

            </div>
          )}

          {/* PROCESSING MESSAGE */}

          {isProcessing && (
            <p>Robot is processing your message...</p>
          )}

          {/* ERROR MESSAGE */}

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

        </section>

      </main>

    </div>
  )
}

export default App