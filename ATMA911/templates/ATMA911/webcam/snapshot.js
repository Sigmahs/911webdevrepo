/*
*  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
*/

// This code is adapted from
// https://rawgit.com/Miguelao/demos/master/mediarecorder.html

'use strict';

/* globals MediaRecorder */

const mediaSource = new MediaSource();
mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
let mediaRecorder;
let sourceBuffer;

const gumVideo = document.querySelector('video#gum');
const canvas = window.canvas = document.querySelector('canvas');
const snapshotButton = document.querySelector('button#snapshot');
snapshotButton.addEventListener('click', () => {
  window.canvas.getContext('2d').drawImage(gumVideo, 0, 0, window.canvas.width, window.canvas.height);
  const img = img || document.querySelector('img');
  let url = window.URL.createObjectURL(blob);
  img.src = url;
  window.URL.revokeObjectURL(url);
});

function handleSourceOpen(event) {
  console.log('MediaSource opened');
  sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
  console.log('Source buffer: ', sourceBuffer);
}

function handleDataAvailable(event) {
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
  }
}

function handleSuccess(stream) {
  snapshotButton.disabled = false;
  console.log('getUserMedia() got stream:', stream);
  window.stream = stream;
  gumVideo.srcObject = stream;
}

async function init(constraints) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
  }
}

document.querySelector('button#start').addEventListener('click', async () => {
  const constraints = {
    audio: {
    },
    video: {
      width: 1280, height: 720
    }
  };
  console.log('Using media constraints:', constraints);
  await init(constraints);
});
