<script setup>
import ml5 from "ml5";
import p5 from "p5";
import {
  Camera,
  CameraResultType,
  CameraSource,
  CameraDirection,
} from "@capacitor/camera";

let img = new Image();
img.src = "images/cat.JPG";
img.width = 640;
img.height = 420;

let video;
let detector;
let detections = [];

let count = 0;

var options = {
  video: {
    facingMode: {
      exact: "environment",
    },
  },
};

const sketch = (s) => {
  s.setup = () => {
    s.createCanvas(640, 420);
    // video = s.createCapture(s.VIDEO, videoReady);
    video = s.createCapture(options, videoReady);
    video.size(640, 420);
    video.hide();
  };

  s.draw = () => {
    s.background(0);
    s.image(video, 0, 0);
    for (let i = 0; i < detections.length; i += 1) {
      const object = detections[i];
      s.stroke(0, 255, 0);
      s.strokeWeight(4);
      s.noFill();
      s.rect(object.x, object.y, object.width, object.height);
      s.noStroke();
      s.fill(255);
      s.textSize(24);
      s.text(object.label, object.x + 10, object.y + 24);
    }
  };
};

function videoReady() {
  // Models available are 'cocossd', 'yolo'
  detector = ml5.objectDetector("cocossd", modelReady);
}

function gotDetections(error, results) {
  if (error) {
    console.error(error);
  }

  // Loop through all the results and check if there is a car
  for (let i = 0; i < results.length; i += 1) {
    const object = results[i];
    if (object.label === "person") {
      console.log("Car detected!");
      takePhoto();
      count += 1;
    }
  }

  detections = results;
  detector.detect(video, gotDetections);
}

function modelReady() {
  detector.detect(video, gotDetections);
}

async function takePhoto() {
  const options = {
    resultType: CameraResultType.Uri,
    source: CameraSource.Camera,
    direction: CameraDirection.Rear,
    saveToGallery: true,
  };
  const originalPhoto = await Camera.getPhoto(options);
  const photoInTempStorage = await Filesystem.readFile({
    path: originalPhoto.path,
  });
  let date = new Date(),
    time = date.getTime(),
    fileName = time + ".jpeg";
  await Filesystem.writeFile({
    data: photoInTempStorage.data,
    path: fileName,
    directory: FilesystemDirectory.Data,
  });
  const finalPhotoUri = await Filesystem.getUri({
    directory: FilesystemDirectory.Data,
    path: fileName,
  });
  let photoPath = Capacitor.convertFileSrc(finalPhotoUri.uri);
  console.log(photoPath);
}

const sketchInstance = new p5(sketch);
</script>

<template>
  <div></div>
</template>

<style>
canvas {
  width: 100% !important;
  height: auto !important;
}
</style>
