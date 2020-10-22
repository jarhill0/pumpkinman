function startup() {
  const button = document.getElementById("mouth-button");
  registerTouchOn(button, openMouth);
  registerTouchOff(button, closeMouth);
}

document.addEventListener("DOMContentLoaded", startup);
