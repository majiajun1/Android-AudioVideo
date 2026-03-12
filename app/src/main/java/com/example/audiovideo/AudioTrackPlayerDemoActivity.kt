package com.example.audiovideo

import android.app.Activity
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import kotlin.math.PI
import kotlin.math.sin

class AudioTrackPlayerDemoActivity : Activity(), View.OnClickListener {

    private var playButton: Button? = null
    private var stopButton: Button? = null

    private var audioData: ShortArray? = null
    private var audioTrack: AudioTrack? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
        }

        playButton = Button(this).apply {
            text = "播放 440Hz 正弦波"
            setOnClickListener(this@AudioTrackPlayerDemoActivity)
        }

        stopButton = Button(this).apply {
            text = "停止播放"
            setOnClickListener(this@AudioTrackPlayerDemoActivity)
            isEnabled = false
        }

        layout.addView(playButton)
        layout.addView(stopButton)

        setContentView(layout)

        audioData = generateSineWave(
            sampleRate = 44100,
            durationSeconds = 3,
            frequency = 440.0
        )
    }

    override fun onClick(v: View?) {
        when (v) {
            playButton -> startPlayback()
            stopButton -> stopPlayback()
        }
    }

    private fun generateSineWave(
        sampleRate: Int,
        durationSeconds: Int,
        frequency: Double
    ): ShortArray {
        val totalSamples = sampleRate * durationSeconds
        val buffer = ShortArray(totalSamples)
        val twoPiF = 2.0 * PI * frequency

        for (i in 0 until totalSamples) {
            val t = i.toDouble() / sampleRate
            val value = sin(twoPiF * t)
            buffer[i] = (value * Short.MAX_VALUE * 0.8).toInt().toShort()
        }

        return buffer
    }

    private fun startPlayback() {
        if (audioData == null || audioTrack != null) {
            return
        }

        val sampleRate = 44100
        val channelConfig = AudioFormat.CHANNEL_OUT_MONO
        val audioFormat = AudioFormat.ENCODING_PCM_16BIT
        val bufferSizeInBytes = audioData!!.size * 2

        val track = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(audioFormat)
                    .setSampleRate(sampleRate)
                    .setChannelMask(channelConfig)
                    .build()
            )
            .setBufferSizeInBytes(bufferSizeInBytes)
            .setTransferMode(AudioTrack.MODE_STATIC)
            .build()

        audioTrack = track

        val writeResult = track.write(audioData!!, 0, audioData!!.size)
        if (writeResult > 0) {
            track.play()
            playButton?.isEnabled = false
            stopButton?.isEnabled = true
        } else {
            track.release()
            audioTrack = null
        }
    }

    private fun stopPlayback() {
        audioTrack?.let { track ->
            if (track.playState == AudioTrack.PLAYSTATE_PLAYING) {
                track.stop()
            }
            track.release()
        }
        audioTrack = null

        playButton?.isEnabled = true
        stopButton?.isEnabled = false
    }

    override fun onDestroy() {
        super.onDestroy()
        stopPlayback()
    }
}
