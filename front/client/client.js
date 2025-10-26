const socket = io();
const peers = {}; // id -> RTCPeerConnection

const joinBtn = document.getElementById("join-btn");
const usernameInput = document.getElementById("username");
const roomInput = document.getElementById("roomid");
const chatSection = document.getElementById("chat-section");
const messagesDiv = document.getElementById("messages");
const msgInput = document.getElementById("msg-input");
const sendBtn = document.getElementById("send-msg");
const usersDiv = document.getElementById("users");
const videoGrid = document.getElementById("video-grid");

let roomId, userName;
let localStream;

if (!localStorage.getItem('auth_token')) {window.location.href = '/registration'}

// Подключаемся к камере и микрофону
async function startMedia() {
  try {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    const videoEl = document.createElement("video");
    videoEl.srcObject = localStream;
    videoEl.autoplay = true;
    videoEl.muted = true;
    videoGrid.appendChild(videoEl);
  } catch (e) {
    alert("Не удалось подключить камеру/микрофон");
    console.error(e);
  }
}

joinBtn.onclick = async () => {
  userName = usernameInput.value.trim();
  roomId = roomInput.value.trim();
  if(!userName || !roomId) return alert("Введите имя и ID комнаты");

  chatSection.style.display = "flex";
  await startMedia();
  socket.emit("join-room", { roomId, userName });
};

// Чат
socket.on("chat-history", (messages) => { messagesDiv.innerHTML = ""; messages.forEach(addMessage); });
socket.on("new-message", addMessage);
sendBtn.onclick = () => {
  const text = msgInput.value.trim();
  if(!text) return;
  socket.emit("send-message", { text, user: userName });
  msgInput.value = "";
};

function addMessage(msg) {
  const div = document.createElement("div");
  div.textContent = msg.user + ": " + msg.text;
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Обновление списка участников
socket.on("users-update", (users) => {
  usersDiv.innerHTML = users.map(u=>u.name).join(", ");
});

// WebRTC
socket.on("user-joined", async ({ id }) => {
  const pc = createPeerConnection(id);
  peers[id] = pc;
  localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  socket.emit("webrtc-offer", { sdp: offer, target: id });
});

socket.on("webrtc-offer", async ({ sdp, from }) => {
  const pc = createPeerConnection(from);
  peers[from] = pc;
  localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
  await pc.setRemoteDescription(new RTCSessionDescription(sdp));
  const answer = await pc.createAnswer();
  await pc.setLocalDescription(answer);
  socket.emit("webrtc-answer", { sdp: answer, target: from });
});

socket.on("webrtc-answer", async ({ sdp, from }) => {
  const pc = peers[from];
  await pc.setRemoteDescription(new RTCSessionDescription(sdp));
});

socket.on("ice-candidate", ({ candidate, from }) => {
  const pc = peers[from];
  if (pc && candidate) pc.addIceCandidate(new RTCIceCandidate(candidate));
});

socket.on("user-left", ({ id }) => {
  if(peers[id]) {
    peers[id].close();
    delete peers[id];
    const video = document.getElementById(id);
    if(video) video.remove();
  }
});

// RTCPeerConnection
function createPeerConnection(id) {
  const pc = new RTCPeerConnection();

  pc.onicecandidate = event => {
    if(event.candidate) {
      socket.emit("ice-candidate", { candidate: event.candidate, target: id });
    }
  };

  pc.ontrack = event => {
    let video = document.getElementById(id);
    if(!video) {
      video = document.createElement("video");
      video.id = id;
      video.autoplay = true;
      videoGrid.appendChild(video);
    }
    video.srcObject = event.streams[0];
  };

  return pc;
}
joinBtn.onclick = async () => {
  userName = usernameInput.value.trim();
  roomId = roomInput.value.trim();
  const password = document.getElementById("room-password").value;

  if(!userName || !roomId || !password) return alert("Введите имя, ID комнаты и пароль");

  chatSection.style.display = "flex";
  await startMedia();

  socket.emit("join-room", { roomId, userName, password });
};

socket.on("password-error", (msg) => {
  alert(msg);
  chatSection.style.display = "none";
});
const avatarInput = document.getElementById("avatar");
let avatarData = null;
avatarInput.onchange = () => {
  const file = avatarInput.files[0];
  const reader = new FileReader();
  reader.onload = (e) => avatarData = e.target.result;
  reader.readAsDataURL(file);
};

// Отправка пароля и аватара при входе
joinBtn.onclick = async () => {
  userName = usernameInput.value.trim();
  roomId = roomInput.value.trim();
  const password = document.getElementById("room-password").value;
  if(!userName || !roomId || !password) return alert("Введите имя, ID комнаты и пароль");

  chatSection.style.display = "flex";
  await startMedia();
  socket.emit("join-room", { roomId, userName, password, avatar: avatarData });
};

// Кнопки камеры и микрофона
document.getElementById("toggle-video").onclick = () => {
  localStream.getVideoTracks()[0].enabled = !localStream.getVideoTracks()[0].enabled;
  socket.emit("update-status", { video: localStream.getVideoTracks()[0].enabled });
};
document.getElementById("toggle-mic").onclick = () => {
  localStream.getAudioTracks()[0].enabled = !localStream.getAudioTracks()[0].enabled;
  socket.emit("update-status", { muted: !localStream.getAudioTracks()[0].enabled });
};

