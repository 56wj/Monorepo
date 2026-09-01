<template>
    <div class="3d">3d</div>
  </template>
  
  <script>
  import * as THREE from "three";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
  import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
  
  export default {
    name: "ThreeDIndex",
    created() {
      console.log(THREE.Scene);
      console.log(OrbitControls);
      console.log(GLTFLoader);
    },
  };
  </script>
  
  <style lang="scss" scoped></style>