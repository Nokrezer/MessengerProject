import { TouchableOpacity, Text, View } from 'react-native';
import { useState, useEffect } from 'react';

import {
  useAudioRecorder,
  AudioModule,
  RecordingPresets,
  setAudioModeAsync,
  useAudioRecorderState,
  useAudioPlayer,
  AudioRecorder,
  AudioPlayer
} from 'expo-audio';

async function startHandler(audioRecorder:AudioRecorder){
    await audioRecorder.prepareToRecordAsync();
    audioRecorder.record();
};

async function stopHandler(audioRecorder:AudioRecorder) {
    await audioRecorder.stop();
}

async function playHandler(player:AudioPlayer, audioRecorder:AudioRecorder){
    player.replace(audioRecorder.uri);
    player.play();
}

export default function testPage(){
    const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
    const player = useAudioPlayer();
    
    return (<View>
        <TouchableOpacity onPress={() => startHandler(audioRecorder)}>
            <Text style={{color:"white"}}>Start</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => stopHandler(audioRecorder)}>
            <Text style={{color:"white"}}>Stop</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => playHandler(player, audioRecorder)}>
            <Text style={{color:"white"}}>Play</Text>
        </TouchableOpacity>
    </View>);
}